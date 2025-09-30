

bouh="$( ps -ef | grep nature )"

nline="$( echo "${bouh}" | grep nature_news_views_rss | wc -l )"
if [ ${nline} -le 2 ]; then
    echo 'Launch RSS daemon.'
    while [ 1 == 1 ]; do
        
        echo "hostname: $(more /etc/hostname)"
        if [ "$( more /etc/hostname )" == 'PC343' ]; then
            conda activate bash
            script_dir=/mnt/c/Users/slemaire/softwares/general
        else
            script_dir=/Users/labo/general
        fi

        python "${script_dir}"/nature_news_views_rss.py #> /dev/null 2>&1
        echo ">>> Update on $(date)"

        sleep 86400 # 24 hours
        # sleep 5
    done
fi


####
