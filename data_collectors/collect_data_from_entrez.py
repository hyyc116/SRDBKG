#coding:utf-8
'''
collecting stroke data from pubmed with e-unilities.

'''
from Bio import Entrez
Entrez.email = 'hyyc116@gmail.com'

def search_pubmed():

    pass


def fecth_abstract_with_pubmed_id():

    pass



def collect_stroke_abstract_data():

    pass



if __name__ == '__main__':
    # collect_stroke_abstract_data()


    handle = Entrez.einfo(db="pubmed")

    record = Entrez.read(handle)

    print record["DbInfo"]["Description"]
    print record["DbInfo"]["Count"]
    print record["DbInfo"]["LastUpdate"]



