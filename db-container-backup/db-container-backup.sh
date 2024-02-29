#!/bin/bash

# DB Container Backup Script Template
# ---
# This backup script can be used to automatically backup databases in docker containers.
# It currently supports mariadb, mysql and bitwardenrs containers.
# 

DAYS=2
BACKUPDIR=/home/xcad/backup


# backup all mysql/mariadb containers

CONTAINER=$(docker ps --format '{{.Names}}:{{.Image}}' | grep 'mysql\|mariadb' | cut -d":" -f1)

echo $CONTAINER

if [ ! -d $BACKUPDIR ]; then
    mkdir -p $BACKUPDIR
fi

for i in $CONTAINER; do
    MYSQL_DATABASE=$(docker exec $i env | grep MYSQL_DATABASE |cut -d"=" -f2-)
    MYSQL_PWD=$(docker exec $i env | grep MYSQL_ROOT_PASSWORD |cut -d"=" -f2-)

for i in $CONTAINER; do
    MYSQL_DATABASE=$(docker exec $i env | grep MYSQL_DATABASE |cut -d"=" -f2-)
    MYSQL_PWD=$(docker exec $i env | grep MYSQL_ROOT_PASSWORD |cut -d"=" -f2-)

    docker exec mysql echo "show databases" | MYSQL_PWD=$MYSQL_PWD mysql -u root -h 127.0.0.1 --port=3306 | while read dbname; \
      do if [ $dbname != "Database" ] && [ $dbname != "information_schema" ] && [ $dbname != "performance_schema" ] && [ $dbname != "sys" ] && [ $dbname != "mysql" ]; then
        docker exec -e MYSQL_DATABASE=$dbname -e MYSQL_PWD=$MYSQL_PWD $i $CONTAINER /usr/bin/mysqldump -u root -h 127.0.0.1 $dbname | gzip > $BACKUPDIR/$CONTAINER-$dbname-$(date +"%Y%m%d%H%M").sql.gz
      fi ; done

    OLD_BACKUPS=$(ls -1 $BACKUPDIR/$i*.gz |wc -l)
    if [ $OLD_BACKUPS -gt $DAYS ]; then
        find $BACKUPDIR -name "$i*.gz" -daystart -mtime +$DAYS -delete
    fi
done


    OLD_BACKUPS=$(ls -1 $BACKUPDIR/$i*.gz |wc -l)
    if [ $OLD_BACKUPS -gt $DAYS ]; then
        find $BACKUPDIR -name "$i*.gz" -daystart -mtime +$DAYS -delete
    fi
done


# bitwarden backup

BITWARDEN_CONTAINERS=$(docker ps --format '{{.Names}}:{{.Image}}' | grep 'bitwardenrs' | cut -d":" -f1)

for i in $BITWARDEN_CONTAINERS; do
    docker exec  $i /usr/bin/sqlite3 data/db.sqlite3 .dump \
        | gzip > $BACKUPDIR/$i-$(date +"%Y%m%d%H%M").sql.gz

    OLD_BITWARDEN_BACKUPS=$(ls -1 $BACKUPDIR/$i*.gz |wc -l)
    if [ $OLD_BITWARDEN_BACKUPS -gt $DAYS ]; then
        find $BACKUPDIR -name "$i*.gz" -daystart -mtime +$DAYS -delete
    fi
done

echo "$TIMESTAMP Backup for Databases completed"
