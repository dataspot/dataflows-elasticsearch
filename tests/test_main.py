import dataflows as DF
from elasticsearch import Elasticsearch
from tableschema_elasticsearch import Storage
from dataflows_elasticsearch import dump_to_es

def test_basic_flow_no_mapping_type():

    data = [
        dict(key='key%04d' % x, value=x)
        for x in range(1000)
    ]

    conn_str = 'localhost:9200'

    DF.Flow(
        data,
        DF.update_resource(-1, name='data'),
        DF.set_primary_key(['key']),
        dump_to_es(
            engine=conn_str,
            indexes=dict(
                test_basic_flow=[dict(
                    resource_name='data'
                )]
            )
        ),
    ).process()

    out = list(Storage(Elasticsearch(hosts=[conn_str])).read('test_basic_flow'))
    assert data == sorted(out, key=lambda r: r['key'])

def test_basic_flow_with_mapping_type():

    data = [
        dict(key='key%04d' % x, value=x)
        for x in range(1000)
    ]

    conn_str = 'localhost:9200'

    DF.Flow(
        data,
        DF.update_resource(-1, name='data'),
        DF.set_primary_key(['key']),
        dump_to_es(
            engine=conn_str,
            indexes=dict(
                test_basic_flow=[dict(
                    doc_type='mydoc',
                    resource_name='data'
                )]
            )
        ),
    ).process()

    out = list(Storage(Elasticsearch(hosts=[conn_str])).read('test_basic_flow', doc_type='mydoc'))
    assert data == sorted(out, key=lambda r: r['key'])

if __name__ == '__main__':
    test_basic_flow_with_mapping_type()
    test_basic_flow_no_mapping_type()