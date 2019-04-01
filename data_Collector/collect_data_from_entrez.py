#coding:utf-8
'''
collecting stroke data from pubmed with e-unilities.

(“stroke”
OR “cerebral infarction”
OR “brain ischemia”
OR “cerebral hemorrhagic”
OR “subarachnoid hemorrhage”)
and (“hand”
OR “arm”
OR “upper extremity”
OR “upper limb”)

corresponding search command

((((((((hand)[Abstract] OR arm)[Abstract] OR upper extremity)[Abstract] OR upper limb))[Abstract] AND (((((stroke)[Abstract] OR cerebral infarction)[Abstract] OR brain ischemia)[Abstract] OR cerebral hemorrhagic)[Abstract] OR subarachnoid hemorrhage)[Abstract]))
OR ((((((hand)[Title] OR arm)[Title] OR upper extremity)[Title] OR upper limb))[Title] AND (((((stroke)[Title] OR cerebral infarction)[Title] OR brain ischemia)[Title] OR cerebral hemorrhagic)[Title] OR subarachnoid hemorrhage)[Title]))

search it from title and abastract in pubmed

and search it in all text in pubmed central

'''
from Bio import Entrez
Entrez.email = 'yourmail@mail.com' ### update your mail
import time
from datetime import datetime
import sys
sys.path.extend(['.','..'])
from paths import PATHS
import os

pmc_term = '((((((((hand)[Abstract] OR arm)[Abstract] OR upper extremity)[Abstract] OR upper limb))[Abstract] AND (((((stroke)[Abstract] OR cerebral infarction)[Abstract] OR brain ischemia)[Abstract] OR cerebral hemorrhagic)[Abstract] OR subarachnoid hemorrhage)[Abstract])) OR ((((((hand)[Title] OR arm)[Title] OR upper extremity)[Title] OR upper limb))[Title] AND (((((stroke)[Title] OR cerebral infarction)[Title] OR brain ischemia)[Title] OR cerebral hemorrhagic)[Title] OR subarachnoid hemorrhage)[Title]))'
pubmed_term = '(((((((hand) OR arm) OR upper extremity) OR upper limb)) AND (((((stroke) OR cerebral infarction) OR brain ischemia) OR cerebral hemorrhagic) OR subarachnoid hemorrhage)))'
def pubmed_info():
    handle = Entrez.einfo(db="pubmed")
    record = Entrez.read(handle)
    print record["DbInfo"]["Description"]
    print record["DbInfo"]["Count"]
    print record["DbInfo"]["LastUpdate"]

def search_pubmed_and_pmc(db,term,outpath,b=0):
    ## search dataset
    search_handle = Entrez.esearch(db=db, term=term,usehistory="y")
    search_results = Entrez.read(search_handle)
    count = int(search_results['Count'])
    print db,'number of result:', count
    # id_list = search_results['IdList']
    search_handle.close()
    ## seesion cookie and query_key
    webenv = search_results["WebEnv"]
    query_key = search_results["QueryKey"]


    batch_size = 1000
    out_handle = open(outpath, "a+")
    start = b
    while start < count:
        end = min(count, start+batch_size)
        print "Going to download record %i to %i" % (start+1, end),datetime.now().strftime( '%Y-%m-%d %H:%M:%S' )
        fetch_handle = Entrez.efetch(db=db, rettype="xml", retmode="text",
                                     retstart=start, retmax=batch_size,
                                     webenv=webenv, query_key=query_key)

        try:
            data = fetch_handle.read()
        except:
            print 'exception retry',start
            continue

        fetch_handle.close()
        out_handle.write(data+'\n')

        time.sleep(1)

        start +=batch_size

    out_handle.close()

def download_data():
    pathObj = PATHS()
    ## create data folder if it do not exist.
    if not os.path.exists(pathObj.DATA_FOLDER):
        os.makedirs(pathObj.DATA_FOLDER)
        print 'create data folder ...'

    search_pubmed_and_pmc('pubmed',pubmed_term,pathObj.PUBMED_XML_FILE)
    search_pubmed_and_pmc('pmc',pubmed_term,pathObj.PMC_XML_FILE)

if __name__ == '__main__':
    download_data()

