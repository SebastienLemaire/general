

bouh="$( ps -ef | grep nature )"

nline="$( echo "${bouh}" | grep nature_news_views_rss | wc -l )"
if [ ${nline} -le 2 ]; then
    echo 'Launch RSS daemon.'
    while [ 1 == 1 ]; do
        python /Users/labo/general/nature_news_views_rss.py > /dev/null 2>&1
        sleep 21600
    done
fi


####
