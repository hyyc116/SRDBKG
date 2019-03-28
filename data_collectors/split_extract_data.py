#coding:utf-8
'''


split data and merge data


'''
from bs4 import BeautifulSoup
import os
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from datetime import datetime

def split_data(path):

    outfilepath = path[:-4]+'_{:}.txt'
    print outfilepath
    index  = 0
    content = ''
    for line in open(path):
        if '<?xml version="1.0" ?>' in line:

            if content!='':
                content+=line
                content = content[:-23]

                open(outfilepath.format(index),'w').write(content)

                print 'spliting index:',index
                index+=1

            content='<?xml version="1.0" ?>'

        else:
            content += line

    open(outfilepath.format(index),'w').write(content)

    print path,'split into',index,'sub files.'

def remove_line_and_tag(content):
    content = content.decode('utf-8', 'ignore')
    content = re.sub(r'\s+',' ',content)
    content = re.sub(r'<.*?>','',content)
    return content.strip()

def extract_title_and_abs_from_pmc(path):
    title = ''
    doi = ''
    abstext = ''
    lines = []
    isabs=False
    for line in open(path):
        line = line.strip()

        if line.startswith('<article-id pub-id-type="doi">'):
            doi = remove_line_and_tag(line)

        if line.startswith('<article-title>'):
            title = remove_line_and_tag(line)

        if line.startswith('<abstract'):
            isabs = True


        if line.endswith('</abstract>'):
            isabs = False

        if isabs:
            abstext+=line

        if line.endswith('</article>'):

            if title!='' and doi!='' and abstext!='':
                abstext = remove_line_and_tag(abstext)
                lines.append([doi,title,abstext])

            title = ''
            doi = ''
            abstext = ''

    return lines


def extract_title_and_abs_from_pubmed(path):
    title = ''
    doi = ''
    abstext = ''
    lines = []
    isabs=False
    for line in open(path):
        line = line.strip()

        if line.startswith('<ArticleId IdType="doi">'):
            doi = remove_line_and_tag(line)

        if line.startswith('<ArticleTitle>'):
            title = remove_line_and_tag(line)

        if line.startswith('<Abstract>'):
            isabs = True


        if line.endswith('</Abstract>'):
            isabs = False

        if isabs:
            abstext+=line

        if line.endswith('</PubmedArticle>'):

            if title!='' and doi!='' and abstext!='':
                abstext = remove_line_and_tag(abstext)
                lines.append([doi,title,abstext])

            title = ''
            doi = ''
            abstext = ''

    return lines

# def extract_title_and_abs_from_pubmed(path):
#     content = str(open(path).read()).encode('utf-8','ignore')
#     # print content[:10]
#     doc = BeautifulSoup(content,'xml')
#     # print 'parsed'
#     for article in doc.select('PubmedArticleSet > PubmedArticle'):
#         pubmed_id = article.select('PMID')[0].string
#         titles = article.select('article-title')
#         if len(titles)==0:
#             continue
#         title = titles[0].string
#         if title is None:
#             continue

#         title = remove_line_and_tag(title)

#         abstexts = article.select('Abstract')
#         if len(abstexts)!=1:
#             continue
#         abstext = str(abstexts[0])
#         abstext = remove_line_and_tag(abstext)

#         yield pubmed_id,title,abstext

def extract_title_and_abs(folder,outpath):
    # logf = open('log.txt','w')
    outfile = open(outpath,'a+')

    doi_set = set([line.strip().split('======')[0] for line in open(outpath)])
    # print extracted_files
    # print ''
    if os.path.isdir(folder):
        folder = folder if folder.endswith('/') else folder+'/'

        # doi_set = set()
        index = 0
        for f in os.listdir(folder):

            if not f.endswith('.txt'):
                continue

            if f.endswith('_DATA.txt'):
                continue

            if f.endswith('_bak.txt'):
                continue

            if f.endswith('stroke.txt'):
                continue

            fpath = folder+f

            index+=1
            print index,'extracting from',fpath,',total number of articles:',len(doi_set),',',datetime.now().strftime( '%Y-%m-%d %H:%M:%S' )

            if 'pmc' in f.lower():
                lines = extract_title_and_abs_from_pmc(fpath)
                out_lines = []
                for doi,title,abstext in lines:
                    if doi in doi_set:
                        continue
                    doi_set.add(doi)
                    out_lines.append('======'.join([doi,title,abstext]))

                outfile.write('\n'.join(out_lines)+'\n')

            if 'pubmed' in f.lower():
                lines= extract_title_and_abs_from_pubmed(fpath)
                out_lines = []
                for doi,title,abstext in lines:
                    if doi in doi_set:
                        continue
                    doi_set.add(doi)
                    out_lines.append('======'.join([doi,title,abstext]))

                outfile.write('\n'.join(out_lines)+'\n')

        print '%d articles unique id and abstract are extracted.'%len(doi_set)
        outfile.close()
    else:
        print 'input is not a directory.'

    # logf.close()


if __name__ == '__main__':

    split_data('../DATA/pmc_data.txt')
    split_data('../DATA/pubmed_data.txt')
    extract_title_and_abs('../DATA','../DATA/stroke.txt')









