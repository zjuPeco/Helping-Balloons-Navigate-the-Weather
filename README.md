# Future Challenge -- Helping Balloons Navigate the Weather

### Data Preparation

1. Put all the original data in the ['dataset'] directory

2. Run all the codes in 

 - ['a. Train data preprocessing.ipynb'] 
 - ['b. Test data preprocessing.ipynb'] 

### Regression

Run all the codes in 

 - ['c. Xgboost_cv_wind.ipynb'] 
 - ['d. Lightgbm_cv_wind.ipynb'] 
 - ['e. Lightgbm_all_wind.ipynb'] 
 - ['f. lightgbm_all_rainfall.ipynb']
 - ['g. Lightgbm_all_time_rainfall.ipynb']
 - ['h. Rainfall_mean.ipynb']

### Path finding

1. Use ['i. PointsFinder.py'] and ['j. Point_finder_Django'] to get the guide points.

(if you want to use ['j. Point_finder_Django'], you should put ['CityData.csv'] in the ['j. Point_finder_Django/data'] directory and put the rain matrix and wind matrix, which are generated in the Regression part, in ['j. Point_finder_Django/data/day[6,7,8,9,10]'], name them ['rain_matrix.pickle'] and ['wind_matrix.pickle'])

2. Run ['k. Path Searching.ipynb'] and ['l. Submit.ipynb'] to get the final results

See [documentation]( https://tianchi.aliyun.com/forum/new_articleDetail.html?spm=5176.8366600.0.0.7f3f311frqsV4b&raceId=231622&postsId=4259) for more details.

A Chineses version of documentation is [here](http://blog.csdn.net/zjupeco/article/details/79423397).



