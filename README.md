# About

The purpose of this project is to utilize a physical characteristic of images (i.e., Photo-Response Non-Uniformity or PRNU) to aid in Source Camera Identification (SCI). The code is broken down into two scripts: (a) explorecams_webscraper.py, and (b) algorithm.py. In (a), this script is made to web scrape specific urls from the https://explorecams.com website for data collection on images from different users. In (b), this script processes the extracted PRNU data of these users (.mat files) and will also return the results of the custom algorithm that is based on location matching and Jaccard similarity for use in the SCI setting.   

# Prerequisites and External Resources
PRNU extraction is not defined within the scope of this repository. For more information and code related on PRNU extraction, please reference the following source: http://dde.binghamton.edu/download/camera_fingerprint/

# explorecams_webscraper.py

To use this script, set the desired url endpoint from the https://explorecams.com website in the url declaration. An example is shown below.

```py
url = 'https://explorecams.com/photos/pair/x-t10=xf18-55mmf2-8-4-r-lm-ois'
```

Next, customize parameters to extract a particular number of users (n) that contain the highest amount of data/images from the explorecams website url. An example is shown below for extracting the top 6 users.

```py
html_data = retrieve_html_source(url, 20)
top_users = top_n_users(html_data, n=6)
```

Lastly, define the local file paths (of folders), in which to save the images to. There should be a folder for each user that is extracted from the explorecams.com website.

```py
dir1 = ''
dir2 = ''
dir3 = ''
dir4 = ''
dir5 = ''
dir6 = ''
```

# algorithm.py

To start, modify the resolution size of your image files under the declaration 'res' and enter your file path or directories for each of your devices/users PRNU .mat files to compare against. An example is shown below for n=6 directories.

```py
# IMAGE RESOLUTION/SIZE MUST BE SET HERE
res = (440, 440)

# USER DIRECTORIES MUST BE SET HERE
user1_dir = ''
user2_dir = ''
user3_dir = ''
user4_dir = ''
user5_dir = ''
user6_dir = ''
```

Once set, modify the NUM_PRNU parameter to the number of PRNU's you wish to randomly extract from your directories.  

```py
NUM_PRNU = 100
```

Next, set your pairwise comparison as follows (can be modified to compare against specific pairs):

As an example, comparing D1 to D2:
```py
D1_D2_train_matches, D1_D1_train_matches, D2_D2_train_matches = device_combinations(
    reduced80_D1_train, reduced80_D2_train, res)
```

Lastly, modify the value of test_num to randomly select a testing set of a given size to evaluate on.  

```py 
test_num = 20
```
