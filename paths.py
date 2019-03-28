#coding:utf-8

'''
定义程序中所有可能用到的路径信息

'''

### 定义所有的
class PATHS:

    def __init__(self,field):
        ## DATA FOLDER
        self.DATA_FOLDER = '../DATA'


        ## PMC XML FILE
        self.PMC_XML_FILE = self.DATA_FOLDER+'/pmc_xml.txt'
        ## PUBMED XML FILE
        self.PUBMED_XML_FILE=self.DATA_FOLDER+'/pubmed_xml.txt'

        ## EXTRACTED DATA FILE
        self.STROKE_DATA_FILE = self.DATA_FOLDER+'/stroke.txt'






