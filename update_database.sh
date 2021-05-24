mkdir -p data
python3 gen_download_links.py -d data -y 5
wget --content-disposition -w 3 -i data/links.txt -P data
