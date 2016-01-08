#!/bin/bash

export TZ=America/Los_Angeles
TOTAL_SIZE_MB=20000
PER_JOB_MB=$(($TOTAL_SIZE_MB / 5))

FIO=result-$(date +%Y-%m-%d)-$(date +%s)

if [ -z `cat /proc/mounts | grep /mnt/myfs > /dev/null`]; then
   mkdir -p /mnt/myfs/${FIO}

   iostat -c -d -x -t -m /dev/sda /dev/sdb /dev/sdc 1 > iostat.out &
   vmstat 1 > vmstat.out &
   date >> fio-${FIO}-result.txt
   fio --name=fio-5 --directory=/mnt/myfs/${FIO} --fallocate=none \
       --rw=write --size=${PER_JOB_MB}M --bs=1M --scramble_buffers=1 \
       --nrfiles=1 --openfiles=1 \
       --ioengine=sync --thread --numjobs=5 --end_fsync=1 >> \
       fio-${FIO}-result.txt
   date >> fio-${FIO}-result.txt
   pkill -f iostat
   pkill -f vmstat
   cat iostat.out >> fio-${FIO}-result.txt
   cat vmstat.out >> fio-${FIO}-result.txt
else
   date
   echo "FS not mounted..."
fi

