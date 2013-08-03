#!/bin/bash

SERVER=127.0.0.1

function request()
{
    local method=$1
    local path=$2
    data=$3

    if [ "$data" != "" ]; then
        data="--data-binary $data"
    fi
    curl -sv -X $method http://$SERVER/$path $data 2>&1
}

function get_result_key()
{
    grep '^{"is_created' | sed 's/[{",:}]//g' | cut -d ' ' -f 2,4
}

function get_redirect()
{
    grep '^< Location:' | sed 's/\r//g' | cut -d ' ' -f 3
}

function get_http_code()
{
    grep '^< HTTP' | cut -d ' ' -f 3
}

function get_stat_numpv()
{
    grep '^{"'|sed 's/[{":,}]//g'|cut -d' ' -f2
}

function test()
{
    local url="$1"
    ret=`request POST "/api/new" "$url" | get_result_key`
    is_created=`echo "$ret" | cut -d ' ' -f1`
    key=`echo "$ret" | cut -d ' ' -f2`

    if [ "$is_created" != "true" ]; then
        echo "new fail on url: $url => $ret"
        return 1
    fi

    if [ "$key" == "null" ] || [ "$key" == "" ]; then
        echo "new fail on url: $url => $ret"
        return 1
    fi

    stat_http_code=`request GET "/api/stat/$key" | get_http_code`
    if [ "$stat_http_code" != "404" ]; then
        echo "stat fail on url: $url => $key -> $stat_http_code"
        return 1
    fi

    redirect=`request GET "/$key"|get_redirect`

    if [ "$url" != "$redirect" ]; then
        echo "redirect fail on url: $url => $redirect"
        return 1
    fi

    request GET "/$key" > /dev/null
    request GET "/$key" > /dev/null
    stat_numpv=`request GET "api/stat/$key" | get_stat_numpv`
    if [ "$stat_numpv" != "3" ]; then
        echo "stat fail on url: $url => $key -> $stat_numpv"
        return 1
    fi

    echo "pass on url: $url"
    return 0
}

function get_url_from_baidunews()
{
    curl -s "http://news.baidu.com" | grep 'href="http'|sed 's/^.*href="//' | cut -d '"' -f 1|grep '^http'
}

function test_by_urllist_file()
{
    cat $1 | while read url ; 
    do
        test "$url"
    done
}

function run_test()
{
    if ! [ -e "/tmp/urllist.txt" ]; then
        get_url_from_baidunews > /tmp/urllist.txt
    fi
    test_by_urllist_file /tmp/urllist.txt
}

if [ $# -eq 0 ]; then
    run_test
    exit
fi

$1 "$2" "$3"

