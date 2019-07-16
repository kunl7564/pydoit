#!/usr/bin/python
#  -*- coding:utf-8 -*-

import time
import Queue
import rf522
import sqlite3
import RPi.GPIO as GPIO
import picamera
import json
import os
import ffmpy
import socket
import struct
import array
import netifaces
import six
import uuid
import copy
import urllib
import urllib2
import smbus
import bluetooth
import threading
import codecs
import pygame
import binascii
import subprocess
from ctypes import *
from datetime import datetime
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
from PIL import Image, ImageDraw, ImageFont, ImageFilter

"""
版本：1.1.0.0.4 
修改日期：2018-06-12
修改内容：
a.添加版本记录
b.添加LCD显示蓝牙&远程开门结果信息
c.添加蓝牙保持可发现状态
"""

SOFTWARE_VERSION = [1,1,0,0,4]

bleWakeTick = 0
BLE_WAKE_CYCLE = 30000

sound_play_q = Queue.Queue(32)
passwd_detect_q = Queue.Queue(32)
card_detect_q = Queue.Queue(32)
record_sig_q = Queue.Queue(32)
tcp_send_q = Queue.Queue(32)
tcp_recv_q = Queue.Queue(32)

TIME_TICK_1S = 1000
TICK_POLL = 10.0

CARD_DETECT_CYCLE = 1000
card_detect_tick = 0

TYPE_PASSWD = 0
TYPE_CARDID = 1
TYPE_REMOTE = 2

DOOR_DETECT = 0

DOOR_PIN = 19
DOOR_OPEN, DOOR_CLOSED, DOOR_KEEP_OPEN = "DOOR_OPEN", "DOOR_CLOSED", "DOOR_KEEP_OPEN"
DOOR_KEEP_OPEN_TIME = 20000
door_open_state = DOOR_CLOSED
door_keep_open_tick = 0

CAMERA_SLEEP, DO_PREPARE, DO_PREPARE_DELAY, CREATE_IMG = "CAMERA_SLEEP", "DO_PREPARE","DO_PREPARE_DELAY","CREATE_IMG"
CREATE_VIDEO, CREATE_VIDEO_DELAY, RECORD_SAVE = "CREATE_VIDEO","CREATE_VIDEO_DELAY","RECORD_SAVE"
DOOROPEN_PREPARE_DELAY_TIME = 2000
DOOROPEN_VIDEO_TIME = 20000
PHOTO_SAVE_PATH = "/home/pi/dev/app/photo/%d.jpg"
VIDEO_SAVE_PATH = "/home/pi/dev/app/video/%d.mp4"
PHOTO_TMP_PATH = "/tmp/photo/%d.jpg"
VIDEO_TMP_264_PATH = "/tmp/video/%d.h264"
VIDEO_TMP_MP4_PATH = "/tmp/video/%d.mp4"
DB_PATH = "/home/pi/dev/app/cfg.db"

record_state = CAMERA_SLEEP
video_tick = 0
prepare_tick = 0
record_time = None

camera = None

MAX_RECORD = 100
record_pool = []
POOL_PATH = "/home/pi/dev/app/pool"
CFG_PATH = "/home/pi/dev/app/cfg.json"

clientsock = None

screen = None

redu = [0x00, 0x00]

proto_version = [0x01]
encrypt_type = [0x01]

MSG_HEATBEAT = [0x00, 0x01]
MSG_HEATBEAT_RSP = [0x80, 0x01]

PASSWD_OPEN = [0x00, 0x02]
PASSWD_OPEN_RSP = [0x80, 0x02]

CARD_OPEN = [0x00, 0x03]
CARD_OPEN_RSP = [0x80, 0x03]

REMOTE_OPEN = [0x00, 0x04]
REMOTE_OPEN_RSP = [0x80, 0x04]

IMG_UPLOAD = [0x00, 0x05]
IMG_UPLOAD_RSP = [0x80, 0x05]

VIDEO_UPLOAD = [0x00, 0x06]
VIDEO_UPLOAD_RSP = [0x80, 0x06]

DIAG_UPLOAD = [0x00, 0xE0]
DIAG_UPLOAD_RSP = [0x80, 0xE0]

SYN_DATABASE = [0x00, 0x07]
SYN_DATABASE_RSP = [0x80, 0x07]

BIN_UPGRADE = [0x00, 0x08]
BIN_UPGRADE_RSP = [0x80, 0x08]

SYN_DB_RESULT = [0x00, 0x0a]
SYN_DB_RESULT_RSP = [0x80, 0x0a]

COMM_CONNECT, COMM_SEND_RECV = "COMM_CONNECT", "COMM_SEND_RECV"
comm_state = COMM_CONNECT

send_img_record_flag = False
send_video_record_flag = False
cardopen_record_rsp_flag = False
passwdopen_record_rsp_flag = False
remoteopen_record_flag = False
syn_db_result_rsp_flag = False

record_timeout_tick = 0

heartbeat_rsp_flag = False
heartbeat_timeout_tick = 0
heartbeat_delay_tick = 0

RECORD_TIMEOUT = 10000
HEARTBEAT_TIMEOUT = 10000
HEARTBEAT_DELAY = 10000

SEND_HEARTBEAT, SEND_HEARTBEAT_RSP, SEND_HEARTBEAT_DELAY = "SEND_HEARTBEAT", "SEND_HEARTBEAT_RSP", "SEND_HEARTBEAT_DELAY"

SEND_DIAG, SEND_DIAG_RSP, SEND_DIAG_DELAY = "SEND_DIAG", "SEND_DIAG_RSP", "SEND_DIAG_DELAY"
DIAG_TIMEOUT = 10000
SEND_DIAG_DELAY = 30000
diag_rsp_flag = False
diag_timeout_tick = 0
diag_delay_tick = 0
send_diag_state = SEND_DIAG

SEND_DELAY = "SEND_DELAY"
SEND_PREPARE = "SEND_PREPARE"
SEND_IMG, SEND_VIDEO = "SEND_IMG", "SEND_VIDEO"
SEND_IMG_RSP, SEND_VIDEO_RSP = "SEND_IMG_RSP", "SEND_VIDEO_RSP"
SEND_IMG_RECORD, SEND_IMG_RECORD_RSP = "SEND_IMG_RECORD", "SEND_IMG_RECORD_RSP"
SEND_VIDEO_RECORD, SEND_VIDEO_RECORD_RSP = "SEND_VIDEO_RECORD", "SEND_VIDEO_RECORD_RSP"
SEND_RECORD, SEND_RECORD_RSP = "SEND_RECORD", "SEND_RECORD_RSP"

send_heartbeat_state = SEND_HEARTBEAT
send_record_state = SEND_PREPARE

DO_SEND_HEARTBEAT = "DO_SEND_HEARTBEAT"
DO_SEND_DIAG = "DO_SEND_DIAG"
DO_SEND_RECORD = "DO_SEND_RECORD"

send_main_state = DO_SEND_HEARTBEAT

do_send_obj = None

LED_PIN = 23
LED_1_PIN = 17

SENSOR_PIN = 4
SENSOR_DETECT_1,SENSOR_DELAY,SENSOR_DETECT_2="SENSOR_DETECT_1","SENSOR_DELAY","SENSOR_DETECT_2"
SENSOR_DETECT_DELAY = 50
sensor_detect_stage = SENSOR_DETECT_1
sensor_detect_tick = 0
sensor_status = False

open_status = False
open_time = 0
open_type = None
open_info = None

STA_OK = [0]

bus = None
keyinput = []
keyscantick = 0
KEY_SCAN_INTERVAL = 100
KV0,KV1,KV2,KV3,KV4,KV5,KV6,KV7,KV8 = "0","1","2","3","4","5","6","7","8"
KV9,KV_CALL,KV_CONFIRM,KV_PRE,KV_DEL = "9","CALL","CONFIRM","PRE","DEL"

KEY_SCAN_0,KEY_SCAN_1="KEY_SCAN_0","KEY_SCAN_1"
KEY_SCAN_2,KEY_SCAN_3="KEY_SCAN_2","KEY_SCAN_3" 
keyscan_stage = KEY_SCAN_0
keyscan_tick = 0
KEYSCAN_DELAY = 30
key_t1 = None
key_t2 = None

LCD_CS = 8
LCD_RST  = 25
LCD_A0 = 24
LCD_CLK = 11
LCD_SI = 10

lcd_flash_tick = 0
LCD_FLASH_CYCLE = 500

SOUND_PLAY_1, SOUND_PLAY_2 = "SOUND_PLAY_1", "SOUND_PLAY_2"
sound_play_stage = SOUND_PLAY_1
SOUND_CLICK = "click"
SOUND_PASS = "pass"
SOUND_FAIL = "fail"

MAX_INPUT = 9

lastdat = 0

static_cfg = """
hostname
clientid
persistent
option rapid_commit
option domain_name_servers, domain_name, domain_search, host_name
option classless_static_routes
option ntp_servers
option interface_mtu
require dhcp_server_identifier
slaac private
interface eth0
static ip_address=%d.%d.%d.%d/%d
static routers=%d.%d.%d.%d
static domain_name_servers=%d.%d.%d.%d
"""

dhcp_cfg = """
hostname
clientid
persistent
option rapid_commit
option domain_name_servers, domain_name, domain_search, host_name
option classless_static_routes
option ntp_servers
option interface_mtu
require dhcp_server_identifier
slaac private
interface eth0
"""

KEY_B = 24
KEY_A = 25
KEY_3 = 1
KEY_2 = 0
KEY_1 = 20
KEY_LED = 23

cfgdbupdate_flag = False
cfgdb_key = None

fwupdate_flag = False
fw_key = None
fw_name = None

bleopen_record_flag = None

background = None

PASSWD_OPEN_SUCCESS_NOTIFY = u"密码开门成功！"
PASSWD_OPEN_FAIL_NOTIFY = u"密码开门失败！"
CARD_OPEN_SUCCESS_NOTIFY = u"刷卡开门成功！"
CARD_OPEN_FAIL_NOTIFY = u"刷卡开门失败！"
BLE_OPEN_SUCCESS_NOTIFY = u"蓝牙开门成功！"
BLE_OPEN_FAIL_NOTIFY = u"蓝牙开门失败！"
REMOTE_OPEN_SUCCESS_NOTIFY = u"远程开门成功！"
REMOTE_OPEN_FAIL_NOTIFY = u"远程开门失败！"

HEADER_DISP = {
    "content":u"TPSON科技",
    "pos":(80,60),
    "font":48,
    "color":(255,255,255)
}

DATETIME_DISP = {
    "content":u"",
    "pos":(80,120),
    "font":28,
    "color":(255,255,255)
}

GUIDE_DISP = {
    "content": u"操作说明",
    "pos": (400, 200),
    "font": 36,
    "color": (255, 0, 0)
}


CARD_OPEN_DISP = {
    "content": u"刷卡开门        将门禁卡靠近感应区",
    "pos": (80, 280),
    "font": 28,
    "color": (0, 0, 255)
}

PASSWORD_OPEN_DISP = {
    "content": u"密码开门        输入8位密码按#键结束，如输入错误按*键清除",
    "pos": (80, 330),
    "font": 28,
    "color": (0, 0, 255)
}


REMOTE_OPEN_DISP = {
    "content": u"远程开门        手机APP呼叫控制中心开门",
    "pos": (80, 380),
    "font": 28,
    "color": (0, 0, 255)
}


NOTIFY_DISP = {
    "content": u"输入提示        ",
    "pos": (80, 470),
    "font": 28,
    "font_ob": None,
    "color": (255, 0, 0)
}

NOTIFYMSG_DISP = {
    "content": u"",
    "pos": (260, 470),
    "font": 28,
    "color": (255, 0, 0)
}


recv_seq_id = [0, 0]
send_seq_id = [0, 0]

current_seq = []
seq_num = 0


def setNotifyMsg(msg):
    global NOTIFYMSG_DISP
    NOTIFYMSG_DISP["content"] = msg

def cleanNotifyMsg():
    global NOTIFYMSG_DISP
    NOTIFYMSG_DISP["content"] = u""

def setKV(k, v):
    with open(CFG_PATH, "r") as f:
        cfg_table = json.loads(f.read())
    cfg_table[k] = v
    dat = json.dumps(cfg_table)
    with open(CFG_PATH, "w") as f:
        f.write(dat)
        
def getKV(k):
    with open(CFG_PATH, "r") as f:
        cfg_table = json.loads(f.read())
    return cfg_table[k]
        
def getDevId():
    t = []
    v = getKV("devid")
    dat = struct.unpack("%dc" % len(v), v)
    for i in range(0, len(v)):
        t.append(six.byte2int(dat[i]))
    return t
    
def getFileKey():
    v = getKV("dbkey")
    return v
    
def getFwKey():
    v = getKV("fwkey")
    return v
    
def getFileUrl(type):
    v = getKV("file_url")
    if type == "img_upload_url":
        return v + "/api/device/v1/door/image/upload"
    elif type == "video_upload_url":
        return v + "/api/device/v1/door/video/upload"
    elif type == "db_get_url":
        return v + "/api/device/v1/door/cfg_db/download"
    else:
        pass
    
def getFwUrl(type):
    v = getKV("fw_url")
    if type == "fw_get_url":
        return v + "/api/device/v1/door/firmware_download"
    elif type == "fw_stat_url":
        return v + "/api/device/v1/door/update_info"
    else:
        pass
    
def getDoorUrl():
    v = getKV("door_url")
    addr = (v.split(":")[0], int(v.split(":")[1]))
    return addr

def getSeq():
    global send_seq_id
    return send_seq_id

def print_ex(dat):
    print datetime.now(),":",dat
    
def add(a, b):
    result = c_int32(a).value + c_int32(b).value
    return c_int32(result).value

def sub(a, b):
    result = c_int32(a).value - c_int32(b).value
    return c_int32(result).value

def rshift(n,i):
    if n<0: n = c_uint32(n).value
    return c_int32(n >> i).value

def lshift(n,i):
    return c_int32(c_int32(n).value << i).value

def xor(a, b, c):
    middle = c_int32(a).value ^ c_int32(b).value
    return c_int32(middle ^ c_int32(c).value).value

class TEA:
    @staticmethod
    def encrypt(v, k):
        v0 = v[0]; v1 = v[1]; sum = 0;
        delta = 0x9e3779b9
        k0 = k[0]; k1 = k[1]; k2 = k[2]; k3 = k[3];
        for i in range(0 , 32):
            sum = add(delta,sum);
            v0 = add(v0,xor(add(lshift(v1, 4), k0), add(v1, sum),add(rshift(v1, 5), k1)))
            v1 = add(v1,xor(add(lshift(v0, 4), k2),add(v0, sum),add(rshift(v0, 5), k3)))
        v[0] = v0
        v[1] = v1
        return v

    @staticmethod
    def decrypt(v, k):
        v0 = v[0]; v1 = v[1]; sum = 0xc6ef3720;
        delta = 0x9e3779b9;
        k0 = k[0]; k1 = k[1]; k2 = k[2]; k3 = k[3];
        for _ in range(0, 32):
            v1 = sub(v1,xor(add(lshift(v0,4), k2),add(v0, sum),add(rshift(v0,5), k3)))
            v0 = sub(v0,xor(add(lshift(v1, 4), k0),add(v1, sum),add(rshift(v1, 5), k1)))
            sum = sub(sum,delta)
        v[0] = v0
        v[1] = v1
        return v
            
def cfgdb_update():
    pass
    
def cfgdb_reinit():
    pass
    
def cfgdb_check(type, val):
    ret = False
    cfgdb_base = sqlite3.connect(DB_PATH).cursor()
    cfgdb_base.execute('Select * From tp_pass')
    for eachUser in cfgdb_base.fetchall():
        if type == TYPE_CARDID:
            if eachUser[1] == type and val == eachUser[0]:
                print_ex('card info match')
                ret = True
        elif type == TYPE_PASSWD:
            if eachUser[1] == type and val == eachUser[0]:
                print_ex('passwd info match')
                ret = True
    return ret
    
def led_on():
    GPIO.output(LED_PIN, True)
    GPIO.output(LED_1_PIN, True)
    
def led_off():
    GPIO.output(LED_PIN, False)
    GPIO.output(LED_1_PIN, False)
    
wCRCTable = [
0X0000, 0XC0C1, 0XC181, 0X0140, 0XC301, 0X03C0, 0X0280, 0XC241,
0XC601, 0X06C0, 0X0780, 0XC741, 0X0500, 0XC5C1, 0XC481, 0X0440,
0XCC01, 0X0CC0, 0X0D80, 0XCD41, 0X0F00, 0XCFC1, 0XCE81, 0X0E40,
0X0A00, 0XCAC1, 0XCB81, 0X0B40, 0XC901, 0X09C0, 0X0880, 0XC841,
0XD801, 0X18C0, 0X1980, 0XD941, 0X1B00, 0XDBC1, 0XDA81, 0X1A40,
0X1E00, 0XDEC1, 0XDF81, 0X1F40, 0XDD01, 0X1DC0, 0X1C80, 0XDC41,
0X1400, 0XD4C1, 0XD581, 0X1540, 0XD701, 0X17C0, 0X1680, 0XD641,
0XD201, 0X12C0, 0X1380, 0XD341, 0X1100, 0XD1C1, 0XD081, 0X1040,
0XF001, 0X30C0, 0X3180, 0XF141, 0X3300, 0XF3C1, 0XF281, 0X3240,
0X3600, 0XF6C1, 0XF781, 0X3740, 0XF501, 0X35C0, 0X3480, 0XF441,
0X3C00, 0XFCC1, 0XFD81, 0X3D40, 0XFF01, 0X3FC0, 0X3E80, 0XFE41,
0XFA01, 0X3AC0, 0X3B80, 0XFB41, 0X3900, 0XF9C1, 0XF881, 0X3840,
0X2800, 0XE8C1, 0XE981, 0X2940, 0XEB01, 0X2BC0, 0X2A80, 0XEA41,
0XEE01, 0X2EC0, 0X2F80, 0XEF41, 0X2D00, 0XEDC1, 0XEC81, 0X2C40,
0XE401, 0X24C0, 0X2580, 0XE541, 0X2700, 0XE7C1, 0XE681, 0X2640,
0X2200, 0XE2C1, 0XE381, 0X2340, 0XE101, 0X21C0, 0X2080, 0XE041,
0XA001, 0X60C0, 0X6180, 0XA141, 0X6300, 0XA3C1, 0XA281, 0X6240,
0X6600, 0XA6C1, 0XA781, 0X6740, 0XA501, 0X65C0, 0X6480, 0XA441,
0X6C00, 0XACC1, 0XAD81, 0X6D40, 0XAF01, 0X6FC0, 0X6E80, 0XAE41,
0XAA01, 0X6AC0, 0X6B80, 0XAB41, 0X6900, 0XA9C1, 0XA881, 0X6840,
0X7800, 0XB8C1, 0XB981, 0X7940, 0XBB01, 0X7BC0, 0X7A80, 0XBA41,
0XBE01, 0X7EC0, 0X7F80, 0XBF41, 0X7D00, 0XBDC1, 0XBC81, 0X7C40,
0XB401, 0X74C0, 0X7580, 0XB541, 0X7700, 0XB7C1, 0XB681, 0X7640,
0X7200, 0XB2C1, 0XB381, 0X7340, 0XB101, 0X71C0, 0X7080, 0XB041,
0X5000, 0X90C1, 0X9181, 0X5140, 0X9301, 0X53C0, 0X5280, 0X9241,
0X9601, 0X56C0, 0X5780, 0X9741, 0X5500, 0X95C1, 0X9481, 0X5440,
0X9C01, 0X5CC0, 0X5D80, 0X9D41, 0X5F00, 0X9FC1, 0X9E81, 0X5E40,
0X5A00, 0X9AC1, 0X9B81, 0X5B40, 0X9901, 0X59C0, 0X5880, 0X9841,
0X8801, 0X48C0, 0X4980, 0X8941, 0X4B00, 0X8BC1, 0X8A81, 0X4A40,
0X4E00, 0X8EC1, 0X8F81, 0X4F40, 0X8D01, 0X4DC0, 0X4C80, 0X8C41,
0X4400, 0X84C1, 0X8581, 0X4540, 0X8701, 0X47C0, 0X4680, 0X8641,
0X8201, 0X42C0, 0X4380, 0X8341, 0X4100, 0X81C1, 0X8081, 0X4040]
    
def getCRC(dat):
    n = 0
    nTemp = 0
    wCRCWord = 0xFFFF
    for i in dat:
        n = n + 1
        nTemp = i ^ wCRCWord
        nTemp &= 0xff
        wCRCWord >>= 8
        wCRCWord ^= wCRCTable[nTemp]
    result = [wCRCWord / 256, wCRCWord % 256]
    return result
    
header = [0x40, 0x40]
proto_type = [0x00]
#seq_id = [0x00, 0x00]

device_type = [0x00, 0x60]
encrypt_redu = [0x0]
msg_id = [0x0, 0x0]
tail = [0x23, 0x23]
key = [0x24, 0x57, 0x21, 0x06]

# 组包函数
def makePkg(msgbody, type, seq_id):
    dat = []
    v = [0, 0]
    crc = [0x0,0x0]
    dlen = [0x00, 0x00]
    dat.extend(header)      # 包头
    dat.extend(proto_type)  # 协议类型
    dat.extend(seq_id)      # 流水号
    dat.extend(getDevId())  # 设备id
    dat.extend(device_type) # 设备类型
    msglen = len(msgbody)
    
    #print msglen
    
    if msglen == 0:
        encrypt_redu[0] = 0
    else:
        encrypt_redu[0] = 8 - (msglen) % 8
    dlen[1] = msglen + encrypt_redu[0]
    dat.extend(encrypt_redu)    # 加密冗余字段
    dat.extend(type)            # 信息体类型
    dat.extend(dlen)            # 信息体长度
    dat.extend(msgbody)         # 信息体内容
    
    for i in range(0, encrypt_redu[0]): # 补齐冗余长度
        dat.append(0)
        
    #print len(dat)
    #print dat
        
    for i in xrange(20, len(dat), 8):   # TEA加密
        v[0] = lshift(dat[i],24) + lshift(dat[i+1],16) + lshift(dat[i+2],8) + lshift(dat[i+3],0)
        v[1] = lshift(dat[i+4],24) + lshift(dat[i+5],16) + lshift(dat[i+6],8) + lshift(dat[i+7],0)
        v[0], v[1] = TEA.encrypt(v, key)
        dat[i],dat[i+1],dat[i+2],dat[i+3] = rshift(v[0],24)&0xff,rshift(v[0],16)&0xff,rshift(v[0],8)&0xff,rshift(v[0],0)&0xff
        dat[i+4],dat[i+5],dat[i+6],dat[i+7] = rshift(v[1],24)&0xff,rshift(v[1],16)&0xff,rshift(v[1],8)&0xff,rshift(v[1],0)&0xff

    crc = getCRC(dat[2:])
    dat.extend(crc)
    dat.extend(tail)
    return array.array('B', dat).tostring()

def makeDiag(time, fw, stat, send_seq_id):
    msgbody = []
    msgbody.extend(time)
    msgbody.extend(fw)
    msgbody.extend(stat)
    print msgbody
    return makePkg(msgbody, DIAG_UPLOAD, send_seq_id)

def makeHeartbeat(send_seq_id):
    msgbody = []
    return makePkg(msgbody, MSG_HEATBEAT, send_seq_id)
    
def makePasswdOpen(passwd, time_t, send_seq_id):
    msgbody = []
    msgbody.extend(passwd)
    msgbody.extend(time_t)
    return makePkg(msgbody, PASSWD_OPEN, send_seq_id)

def makeCardOpen(cardid_t, time_t, send_seq_id):
    msgbody = []
    msgbody.extend(cardid_t)
    msgbody.extend(time_t)
    return makePkg(msgbody, CARD_OPEN, send_seq_id)

def makeImgUploadStatus(time_t, sta, uuid, send_seq_id):
    msgbody = []
    msgbody.extend(time_t)
    msgbody.extend(sta)
    msgbody.extend(uuid)
    return makePkg(msgbody, IMG_UPLOAD, send_seq_id)

def makeVideoUploadStatus(time_t, sta, uuid, send_seq_id):
    msgbody = []
    msgbody.extend(time_t)
    msgbody.extend(sta)
    msgbody.extend(uuid)
    return makePkg(msgbody, VIDEO_UPLOAD, send_seq_id)
    
def makeRemoteOpenRsp(time_t, sta, recv_seq_id):
    msgbody = []
    msgbody.extend(time_t)
    msgbody.extend(sta)
    return makePkg(msgbody, REMOTE_OPEN_RSP, recv_seq_id)
    
def makeSyncBaseRsp(recv_seq_id):
    msgbody = []
    return makePkg(msgbody, SYN_DATABASE_RSP, recv_seq_id)

def makeSyncBaseResult(seq, stat, key, send_seq_id):
    msgbody = []
    msgbody.extend([1])
    msgbody.extend(stat)
    msgbody.extend(key)
    return makePkg(msgbody, SYN_DB_RESULT, send_seq_id)
    
def makeBinUpgradeRsp(recv_seq_id):
    msgbody = []
    return makePkg(msgbody, BIN_UPGRADE_RSP, recv_seq_id)
    
def do_openDoor():
    print_ex("do_openDoor")
    GPIO.output(DOOR_PIN, True)
    
def do_closeDoor():
    print_ex("do_closeDoor")
    GPIO.output(DOOR_PIN, False)
    
def start_ble_open():
    global door_open_state
    global open_status
    open_status = True
    door_open_state = DOOR_OPEN
    print_ex("start_ble_open")
    
def start_remote_open(type, info, timestamp):
    global door_open_state
    global open_status
    global open_time
    global open_info
    global open_type
    door_open_state = DOOR_OPEN
    open_status = True
    open_time = timestamp
    open_type = type
    open_info = info
    print_ex("start_remote_open")
    
def start_door_open(type, info, timestamp):
    global door_open_state
    global open_status
    global open_time
    global open_info
    global open_type
    door_open_state = DOOR_OPEN
    open_status = True
    open_time = timestamp
    open_type = type
    open_info = info
    print_ex("start_door_open")
    
def start_passwd_open(type, info, timestamp):
    global door_open_state
    global open_status
    global open_time
    global open_info
    global open_type
    door_open_state = DOOR_OPEN
    open_status = True
    open_time = timestamp
    open_type = type
    open_info = info
    print_ex("start_passwd_open")
    
def stop_door_open():
    do_closeDoor()
    print_ex("stop_door_open")
    
def start_record(type, info, timestamp):
    dat = (type, info, timestamp)
    if record_sig_q.full() == False:
        record_sig_q.put(dat)
    
def camera_init():
    global camera
    camera = picamera.PiCamera()
    camera.resolution = (1024, 768)
    camera.framerate = 24
    
def record_pool_init():
    if os.path.exists(POOL_PATH) == False:
        dat = {
            "type":None,
            "timestamp":None, 
            "imgPath":None, 
            "videoPath":None, 
            "info":None, 
            "uploadflag":None, 
            "index":0,
            "uuid":None
        }
        for i in range(0, MAX_RECORD):
            dat["index"] = i
            record_pool.append(copy.deepcopy(dat))
        dat = json.dumps(record_pool)
        with open(POOL_PATH, "w") as f:
            f.write(dat)
        print_ex("create pool file")
        
def saveRecord(type, info, uuid, time_t, img, video):
    with open(POOL_PATH, "r") as f:
        pool_table = json.loads(f.read())
    for i in pool_table:
        if i["uploadflag"] == None:
            i["uploadflag"] = False
            i["timestamp"] = time_t
            i["type"] = type
            i["imgPath"] = img
            i["videoPath"] = video
            i["uuid"] = uuid
            i["info"] = i["type"] != TYPE_REMOTE and info or None
            break;
    dat = json.dumps(pool_table)
    with open(POOL_PATH, "w") as f:
        f.write(dat)
    
def h264ConvMp4(h264_path, mp4_path):
    ff = ffmpy.FFmpeg(
        inputs = {h264_path: None}, 
        outputs = {mp4_path: ['-vcodec', 'copy', '-f', 'mp4']
    })    
    ff.run()
    os.remove(h264_path)
    
def record_poll(tick):
    global record_state
    global prepare_tick
    global video_tick
    global sensor_status
    global open_status
    global open_time
    global open_info
    global open_type
    global record_time
    
    if record_state == CAMERA_SLEEP:
        if sensor_status == True:       # 红外传感检测到人接近标志
            record_state = DO_PREPARE
            record_time = int(time.time())  # 准备开始记录，记录当前时间
            os.system('rm -fr /tmp/video/')
            os.system('rm -fr /tmp/photo/')
            os.system('mkdir /tmp/video/')
            os.system('mkdir /tmp/photo/')
    elif record_state == DO_PREPARE:
        print_ex("DO_PREPARE")
        prepare_tick = 0
        video_tick = 0
        record_state = DO_PREPARE_DELAY
    elif record_state == DO_PREPARE_DELAY:
        prepare_tick += tick
        if prepare_tick >= DOOROPEN_PREPARE_DELAY_TIME:
            prepare_tick = 0
            record_state = CREATE_IMG
    elif record_state == CREATE_IMG:
        print_ex("CREATE_IMG")
        camera.capture(PHOTO_TMP_PATH % record_time)    # 抓取一张照片
        record_state = CREATE_VIDEO
    elif record_state == CREATE_VIDEO:
        print_ex("CREATE_VIDEO")
        camera.start_recording(VIDEO_TMP_264_PATH % record_time)    # 开始录像
        record_state = CREATE_VIDEO_DELAY
    elif record_state == CREATE_VIDEO_DELAY:
        video_tick += tick
        if video_tick >= DOOROPEN_VIDEO_TIME:   # 录像20s
            camera.stop_recording()     # 结束录像
            h264ConvMp4(VIDEO_TMP_264_PATH % record_time, VIDEO_TMP_MP4_PATH % record_time)  # 视频文件转换为mp4格式
            record_state = RECORD_SAVE
            print_ex("CREATE_VIDEO_DELAY")
    elif record_state == RECORD_SAVE:
        led_off()   # 摄像头照明关闭
        sensor_status = False
        if True == open_status:
            # 如果检测到人接近，且发生了开门操作才保存此次图片视频数据
            print_ex("RECORD_SAVE")
            os.system('cp %s %s' % (PHOTO_TMP_PATH % record_time, PHOTO_SAVE_PATH % record_time))
            os.system('cp %s %s' % (VIDEO_TMP_MP4_PATH % record_time, VIDEO_SAVE_PATH % record_time))
            saveRecord(
                open_type, 
                open_info, 
                str(uuid.uuid1()),
                open_time, 
                PHOTO_SAVE_PATH % record_time, 
                VIDEO_SAVE_PATH % record_time
            )
        record_state = CAMERA_SLEEP
    else:
        pass
    
def doorCtrlPoll(tick):
    global door_open_state
    global door_keep_open_tick
    if door_open_state == DOOR_CLOSED:
        pass
    elif door_open_state == DOOR_OPEN:
        do_openDoor()   # 开门
        door_keep_open_tick = 0
        door_open_state = DOOR_KEEP_OPEN
    elif door_open_state == DOOR_KEEP_OPEN:
        door_keep_open_tick += tick
        if door_keep_open_tick >= DOOR_KEEP_OPEN_TIME:  # 开门保持20s
            do_closeDoor()  # 关门
            door_keep_open_tick = 0;
            door_open_state = DOOR_CLOSED
    else:
        pass
    
def cardDetectPoll(tick):
    global card_detect_tick
    card_detect_tick += tick
    if card_detect_tick >= CARD_DETECT_CYCLE:   # 每秒检测一次
        card_detect_tick = 0
        dat = rf522.read()  # 读卡
        if dat and card_detect_q.full() == False:
            #读到卡数据，格式转换为hex字符串，传入队列
            x = [dat[0], dat[1], dat[2], dat[3]]
            y = str(bytearray(x))
            ss = binascii.b2a_hex(y)
			ss = "43F7E32E"
            #print ss
            card_detect_q.put(ss)

def comm_doRecv():
    global comm_state
    global clientsock
    if comm_state == COMM_CONNECT:  
        try:
            time.sleep(10)
            print "COMM_CONNECT"
            server_addr = getDoorUrl()
            comm_state = COMM_SEND_RECV
            clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientsock.connect(server_addr) # TCP连接，阻塞操作，成功或失败后返回
            #clientsock.settimeout(0)
            #print "COMM_CONNECT"
        #except socket.gaierror as e:
        except Exception, e:
            comm_state = COMM_CONNECT   # 连接失败，重连
            print_ex("Address-related error connecting to server: %s" % e)
    elif comm_state == COMM_SEND_RECV:
        if tcp_recv_q.full() == False:
            try:
                dat = clientsock.recv(4096) # 数据接收，存队列
                #print dat
                if dat:
                    #print_ex("recv %s" % repr(dat))
                    tcp_recv_q.put(dat)
                else:
                    clientsock.close()  # 数据接收异常，关闭连接重连
                    comm_state = COMM_CONNECT
            #except socket.error as e:
            except Exception, e:
                comm_state = COMM_CONNECT
                clientsock.close()
                print "Error receiving data: %s" % e
    else:
        pass

# tcp数据接收线程
def comm_recv(tick):
    while True:
        comm_doRecv()
        time.sleep(tick / TIME_TICK_1S)

def comm_doSend():
    global clientsock
    if tcp_send_q.empty() == False: # 查询发送队列
        dat = tcp_send_q.get()
        try:
            #print_ex("send %s" % repr(dat))
            if clientsock:
                clientsock.send(dat)    # 数据发送
        except socket.error as e:
            clientsock.close()      # 发送异常，关闭连接
            print "Error sending data: %s" % e

# TCP数据发送线程
def comm_send(tick):
    while True:
        comm_doSend()
        time.sleep(tick / TIME_TICK_1S)

"""
def do_commPoll(tick):
    global comm_state, clientsock
    if comm_state == COMM_CONNECT:
        try:
            server_addr = getDoorUrl()
            #print "server_addr", server_addr
            comm_state = COMM_SEND_RECV
            clientsock.connect(server_addr)
            clientsock.settimeout(0)
        except socket.gaierror as e:
            comm_state = COMM_CONNECT
            print_ex("Address-related error connecting to server: %s" % e)
    elif comm_state == COMM_SEND_RECV:
        if tcp_recv_q.full() == False:
            try:
                dat = clientsock.recv(4096)
                if dat:
                    #print_ex("recv %s" % repr(dat))
                    tcp_recv_q.put(dat)
            except socket.error as e:
                comm_state = COMM_CONNECT
                print "Error receiving data: %s" % e
                pass
            
        if tcp_send_q.empty() == False:
            dat = tcp_send_q.get()
            try:
                #print_ex("send %s" % repr(dat))
                clientsock.send(dat)
            except socket.error as e:
                comm_state = COMM_CONNECT
                print "Error sending data: %s" % e
                pass
    else:
        pass
"""
        
def datConv(dat):
    t = []
    v = [0, 0]
    dat = struct.unpack("%dc" % len(dat), dat)
    for i in range(0, 20):
        t.append(six.byte2int(dat[i]))
    for i in xrange(20, len(dat) - 4, 8):
        v[0] = lshift(six.byte2int(dat[i]),24) + lshift(six.byte2int(dat[i+1]),16) + lshift(six.byte2int(dat[i+2]),8) + lshift(six.byte2int(dat[i+3]),0)
        v[1] = lshift(six.byte2int(dat[i+4]),24) + lshift(six.byte2int(dat[i+5]),16) + lshift(six.byte2int(dat[i+6]),8) + lshift(six.byte2int(dat[i+7]),0)
        v[0], v[1] = TEA.decrypt(v, key)
        t.append(rshift(v[0],24)&0xff)
        t.append(rshift(v[0],16)&0xff)
        t.append(rshift(v[0],8)&0xff)
        t.append(rshift(v[0],0)&0xff)
        t.append(rshift(v[1],24)&0xff)
        t.append(rshift(v[1],16)&0xff)
        t.append(rshift(v[1],8)&0xff)
        t.append(rshift(v[1],0)&0xff)
    return t
    
def insert_q(q, dat):
    if q.full() == False:
        q.put(dat)
        
def get_q(q):
    dat = None
    if q.empty() == False:
        dat = q.get()
    return dat

def timestamp_datetime(value):
    format = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(value)
    dt = time.strftime(format, value)
    return dt

def setSysClock(value):
    dt = timestamp_datetime(value)
    #print "setSysClock", dt
    os.system('date -s "%s"' % dt)
        
def getKey(type):
    if type == "dbkey":
        return getFileKey()
    else:
        return getFwKey()
        
def checkCRC(dat):
    t = []
    ss = struct.unpack("%dc" % len(dat), dat)
    for i in range(0, len(dat)):
        t.append(six.byte2int(ss[i]))
    crc1 =  t[-4:-2]
    crc2 = getCRC(t[2:-4])
    if crc1 == crc2:
        return True
    else:
        print "crc fail"
        return False
        
        
def phaseAckPoll(tick):
    global tcp_recv_q
    global heartbeat_rsp_flag
    global cardopen_record_rsp_flag
    global passwdopen_record_rsp_flag
    global remoteopen_record_flag
    global send_img_record_flag
    global send_video_record_flag
    global cfgdbupdate_flag
    global cfgdb_key
    global fwupdate_flag
    global fw_key
    global fw_name
    global syn_db_result_rsp_flag
    global recv_seq_id
    global diag_rsp_flag

    t = None
    dat = get_q(tcp_recv_q) # 从队列读取数据
    if dat:
        if checkCRC(dat) == False:  # CRC校验
            return
        t = datConv(dat)    # 数据解密
        mt = t[16:18]
        recv_seq_id = t[3:5]
        
        if mt == MSG_HEATBEAT_RSP:  # 收到心跳应答
            heartbeat_rsp_flag = True
            tt = lshift(t[20],24)+lshift(t[21],16)+lshift(t[22],8)+t[23] # 平台下发的时间数据
            setSysClock(tt) # 将时间同步到系统时间
        elif mt == PASSWD_OPEN_RSP: # 收到密码开门记录上送应答
            passwdopen_record_rsp_flag = True
            print_ex("get PASSWD_OPEN_RSP")
        elif mt == CARD_OPEN_RSP:    # 收到刷卡开门记录上送应答
            cardopen_record_rsp_flag = True
            print_ex("get CARD_OPEN_RSP")
        elif mt == REMOTE_OPEN:     # 收到远程开门请求
            print_ex("get REMOTE_OPEN")
            remoteopen_record_flag = True   # 触发远程开门操作
            dat = makeRemoteOpenRsp(timeconv(int(time.time())), [1], recv_seq_id)
            insert_q(tcp_send_q, dat)
        elif mt == IMG_UPLOAD_RSP:  # 收到图像数据上送确认应答
            send_img_record_flag = True
            print_ex("get IMG_UPLOAD_RSP")
        elif mt == VIDEO_UPLOAD_RSP:     # 收到视频数据上送确认应答
            send_video_record_flag = True
            print_ex("get VIDEO_UPLOAD_RSP")
        elif mt == SYN_DATABASE:         # 收到平台下发数据库同步请求
            print_ex("get SYN_DATABASE")
            cfgdbupdate_flag = True
            cfgdb_key = ''.join([chr(i) for i in t[20:28]])  # 保存数据库同步key
            setKV("dbkey", cfgdb_key)
            dat = makeSyncBaseRsp(recv_seq_id)
            insert_q(tcp_send_q, dat)
        elif mt == DIAG_UPLOAD_RSP: # 收到诊断数据上送应答
            diag_rsp_flag = True
            print_ex("get DIAG_UPLOAD_RSP")
        elif mt == BIN_UPGRADE:     # 收到固件升级请求
            fw_name = t[20:25]
            dat = makeBinUpgradeRsp(recv_seq_id)
            insert_q(tcp_send_q, dat)
            fwupdate_flag = True    # 触发固件升级
            print_ex("get BIN_UPGRADE")
        elif mt == SYN_DB_RESULT_RSP:   # 收到同步数据库确认应答
            syn_db_result_rsp_flag = False
            print_ex("get SYN_DB_RESULT_RSP")
        else:
            pass
    return t

def getDoorStats():
    #ss = GPIO.input(DOOR_DETECT)
    ss = 1
    print ss
    if ss == 1:
        return [1]
    else:
        return [0]

def getSendSeq():
    global send_seq_id
    send_seq_id[1] += 1
    send_seq_id[1] &= 0xFF
    return send_seq_id

def getFWversion():
    global SOFTWARE_VERSION
    return SOFTWARE_VERSION

def send_diag_poll(tick):
    global diag_rsp_flag
    global diag_timeout_tick
    global diag_delay_tick
    global send_diag_state
    ret = False
    # 发送诊断数据-等待应答-延时
    if send_diag_state == SEND_DIAG:
        send_diag_state = SEND_DIAG_RSP
        diag_rsp_flag = False
        diag_timeout_tick = 0
        dat = makeDiag(timeconv(int(time.time())), getFWversion(), getDoorStats(), getSendSeq())
        insert_q(tcp_send_q, dat)
        print_ex("send SEND_DIAG")
    elif send_diag_state == SEND_DIAG_RSP:
        if diag_rsp_flag == True:
            print_ex("get SEND_DIAG_RSP")
            diag_delay_tick = 0
            send_diag_state = SEND_DIAG_DELAY
            ret = True
        else:
            diag_timeout_tick += tick
            if diag_timeout_tick >= DIAG_TIMEOUT:
                send_diag_state = SEND_DIAG
                print_ex("DIAG_TIMEOUT")
    elif send_diag_state == SEND_DIAG_DELAY:
        diag_delay_tick += tick
        if diag_delay_tick >= SEND_DIAG_DELAY:
            send_diag_state = SEND_DIAG
            print_ex("SEND_DIAG_DELAY")
    return ret

def send_heartbeat_poll(tick):
    global heartbeat_rsp_flag
    global heartbeat_timeout_tick
    global heartbeat_delay_tick
    global send_heartbeat_state
    ret = False
    # 发送心跳数据-等待应答-延时
    if send_heartbeat_state == SEND_HEARTBEAT:
        send_heartbeat_state = SEND_HEARTBEAT_RSP
        heartbeat_rsp_flag = False
        heartbeat_timeout_tick = 0
        seq = getSendSeq()
        dat = makeHeartbeat(seq)
        insert_q(tcp_send_q, dat)
        print_ex("send SEND_HEARTBEAT")
    elif send_heartbeat_state == SEND_HEARTBEAT_RSP:
        if heartbeat_rsp_flag == True:
            print_ex("get MSG_HEATBEAT_RSP")
            heartbeat_delay_tick = 0
            send_heartbeat_state = SEND_HEARTBEAT_DELAY
            ret = True
        else:
            heartbeat_timeout_tick += tick
            if heartbeat_timeout_tick >= HEARTBEAT_TIMEOUT:
                send_heartbeat_state = SEND_HEARTBEAT
                print_ex("HEARTBEAT_TIMEOUT")
    elif send_heartbeat_state == SEND_HEARTBEAT_DELAY:
        heartbeat_delay_tick += tick
        if heartbeat_delay_tick >= HEARTBEAT_DELAY:
            send_heartbeat_state = SEND_HEARTBEAT
            print_ex("HEARTBEAT_DELAY")
    return ret

def checkRecord():
    ret = None
    with open(POOL_PATH, "r") as f:
        pool_table = json.loads(f.read())
    for i in pool_table:
        if i["uploadflag"] == False:
            ret = i
    return ret
    
def markDone(record):
    with open(POOL_PATH, "r") as f:
        pool_table = json.loads(f.read())
    for i in pool_table:
        if i["index"] == record["index"]:
            i["uploadflag"] = None
            break
    dat = json.dumps(pool_table)
    with open(POOL_PATH, "w") as f:
        f.write(dat)

def sendImg(path, uuid):
    res = None
    ret = False
    abs_path = os.path.dirname(path)
    filename = path[len(abs_path)+1:]
    current_path = os.getcwd()
    os.chdir(abs_path)
    print filename
    file = {
        "fileName":filename,
        "image":open(filename, "rb"),
        'device':getDevId(),
        'uid':uuid
    }
    datagen, headers = multipart_encode(file)
    request = urllib2.Request(getFileUrl("img_upload_url"), datagen, headers)
    cfgdb_key = getKey("dbkey")
    request.add_header('tpson_door', cfgdb_key)
    try:
        res = urllib2.urlopen(request).read()
    except:
        res = None
    if res:
        t = json.loads(res)
        if t["code"] == 0:
            ret = True
    os.chdir(current_path)
    return ret
    
def sendVideo(path, uuid):
    res = None
    ret = False
    abs_path = os.path.dirname(path)
    filename = path[len(abs_path)+1:]
    current_path = os.getcwd()
    os.chdir(abs_path)
    file = {
        "fileName":filename,
        "video":open(filename, "rb"),
        'device':getDevId(),
        'uid':uuid
    }
    datagen, headers = multipart_encode(file)
    request = urllib2.Request(getFileUrl("video_upload_url"), datagen, headers)
    cfgdb_key = getKey("dbkey")
    request.add_header('tpson_door', cfgdb_key)
    try:
        res = urllib2.urlopen(request).read()
    except:
        res = None
    if res:
        t = json.loads(res)
        if t["code"] == 0:
            ret = True
    os.chdir(current_path)
    return ret

def timeconv(time):
    time_t = []
    time_t.append(rshift(time, 24) & 0xff)
    time_t.append(rshift(time, 16) & 0xff)
    time_t.append(rshift(time, 8) & 0xff)
    time_t.append(rshift(time, 0) & 0xff)
    return time_t

def idconv(id):
    id_t = []
    t = list(id)
    for i in t:
        id_t.append(ord(i))
    return id_t

def uuidconv(uuid):
    return idconv(uuid)

def sendUploadImgStatus(record):
    time_t = timeconv(record["timestamp"])
    uuid = uuidconv(record["uuid"])
    dat = makeImgUploadStatus(time_t, STA_OK, uuid, getSendSeq())
    insert_q(tcp_send_q, dat)

def sendUploadVideoStatus(record):
    time_t = timeconv(record["timestamp"])
    uuid = uuidconv(record["uuid"])
    dat = makeVideoUploadStatus(time_t, STA_OK, uuid, getSendSeq())
    insert_q(tcp_send_q, dat)

def sendRecord(record):
    global current_seq
    if record["type"] == TYPE_PASSWD:   # 本条记录类型：密码开门
        time_t = timeconv(record["timestamp"])
        passwd = idconv(record["info"])
        dat = makePasswdOpen(passwd, time_t, getSendSeq())
        insert_q(tcp_send_q, dat)
    elif record["type"] == TYPE_CARDID: # 本条记录类型：刷卡开门
        id_t = idconv(record["info"])
        print id_t
        time_t = timeconv(record["timestamp"])
        print time_t
        dat = makeCardOpen(id_t, time_t, getSendSeq())
        insert_q(tcp_send_q, dat)
    elif record["type"] == TYPE_REMOTE: # 远程开门平台自己记录
        pass

SEND_DELAY_TIMEOUT = 3000
send_delay_tick = 0

def send_record_poll(tick):
    global send_record_state
    global do_send_obj
    global cardopen_record_rsp_flag
    global record_timeout_tick
    global send_img_record_flag
    global send_video_record_flag
    global passwdopen_record_rsp_flag
    global send_delay_tick
    ret = False

    if send_record_state == SEND_PREPARE:
        send_delay_tick += tick
        if send_delay_tick >= SEND_DELAY_TIMEOUT:   # 每3s查询一次
            send_delay_tick = 0
            do_send_obj = checkRecord()     # 查询记录池是否有未上送数据
            if do_send_obj:
                send_record_state = SEND_IMG    # 有未上送数据，启动上送流程
                print_ex("SEND_PREPARE")
            else:
                ret = True
    elif send_record_state == SEND_IMG:
        if True == sendImg(do_send_obj["imgPath"], do_send_obj["uuid"]):     # 上送图片数据
             send_record_state = SEND_IMG_RECORD
             print_ex("SEND_IMG ")
        else:
            print_ex("SEND_IMG fail")
            send_record_state = SEND_PREPARE
            
    elif send_record_state == SEND_IMG_RECORD:
        send_img_record_flag = False
        record_timeout_tick = 0
        sendUploadImgStatus(do_send_obj)    # 发送图片上送确认信息
        send_record_state = SEND_IMG_RECORD_RSP
        print_ex("SEND_IMG_RECORD")
        
    elif send_record_state == SEND_IMG_RECORD_RSP:
        if send_img_record_flag == True:
            send_record_state = SEND_VIDEO  # 收到图片上送确认应答
        else:
            record_timeout_tick += tick
            if record_timeout_tick >= RECORD_TIMEOUT:
                print_ex("SEND_IMG_RECORD_TIMEOUT")
                send_record_state = SEND_PREPARE
            
    elif send_record_state == SEND_VIDEO:
        if True == sendVideo(do_send_obj["videoPath"], do_send_obj["uuid"]):    # 发送视频数据
             send_record_state = SEND_VIDEO_RECORD
             print_ex("SEND_VIDEO")
        else:
            send_record_state = SEND_PREPARE

        
    elif send_record_state == SEND_VIDEO_RECORD:
        send_video_record_flag = False
        record_timeout_tick = 0
        sendUploadVideoStatus(do_send_obj)  # 发送视频上送确认信息
        send_record_state = SEND_VIDEO_RECORD_RSP
        print_ex("SEND_VIDEO_RECORD")
        
    elif send_record_state == SEND_VIDEO_RECORD_RSP:
        if send_video_record_flag == True:
             send_record_state = SEND_RECORD    # 收到视频上送确认应答
        else:
            record_timeout_tick += tick
            if record_timeout_tick >= RECORD_TIMEOUT:
                print_ex("SEND_VIDEO_RECORD_TIMEOUT")
                send_record_state = SEND_PREPARE
        
    elif send_record_state == SEND_RECORD:
        cardopen_record_rsp_flag = False
        passwdopen_record_rsp_flag = False
        record_timeout_tick = 0
        sendRecord(do_send_obj)     # 发送开门记录
        send_record_state = SEND_RECORD_RSP
        print_ex("SEND_RECORD")
        
    elif send_record_state == SEND_RECORD_RSP:
        if do_send_obj["type"] == TYPE_PASSWD:
            if passwdopen_record_rsp_flag == True:  # 收到开门记录上送应答
                send_record_state = SEND_PREPARE
                markDone(do_send_obj)   # 将记录信息标志为旧
                ret = True
            else:
                record_timeout_tick += tick
                if record_timeout_tick >= RECORD_TIMEOUT:
                    print_ex("TYPE_PASSWD RECORD_TIMEOUT")
                    send_record_state = SEND_PREPARE
        elif do_send_obj["type"] == TYPE_CARDID:
            if cardopen_record_rsp_flag == True:
                send_record_state = SEND_PREPARE
                markDone(do_send_obj)
                ret = True
            else:
                record_timeout_tick += tick
                if record_timeout_tick >= RECORD_TIMEOUT:
                    print_ex("TYPE_CARDID RECORD_TIMEOUT")
                    send_record_state = SEND_PREPARE
    return ret
    
    
def do_mainPoll(tick):
    send_heartbeat_poll(tick)       # 周期发送心跳数据
    send_diag_poll(tick)            # 周期发送诊断数据
    send_record_poll(tick)          # 周期发送（密码、刷卡）开门记录

def cfgdb_checkPoll(tick):
    if card_detect_q.empty() == False:
        id = card_detect_q.get()    # 从卡检测队列取出
        if True == cfgdb_check(TYPE_CARDID, id):    # 和数据库的卡号比较 
            setNotifyMsg(CARD_OPEN_SUCCESS_NOTIFY)  # 更新LCD显示刷卡开门成功
            # 数据库存在卡号匹配，启动刷卡开门
            start_door_open(TYPE_CARDID, id, int(time.time()))
        else:
            # 数据库不存在该卡，更新LCD显示刷卡开门失败
            setNotifyMsg(CARD_OPEN_FAIL_NOTIFY)
    
def gpio_init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
def lcd_init():
    global screen
    global HEADER
    global DATETIME
    global GUIDE
    global CARD_OPEN
    global PASSWORD_OPEN
    global REMOTE_OPEN
    global NOTIFY
    global NOTIFYMSG
    global background
    pygame.init()
    screen = pygame.display.set_mode((1024, 600))
    background_image_filename = '/home/pi/dev/app/xp.bmp'
    background = pygame.image.load(background_image_filename).convert()
    #display_table = [HEADER, DATETIME, GUIDE, CARD_OPEN, PASSWORD_OPEN, REMOTE_OPEN, NOTIFY, NOTIFYMSG]
    #for i in display_table:
    #    i["font_ob"] = pygame.font.Font('/home/pi/dev/app/msyh.ttf', i["font"]),
    
def door_init():
    GPIO.setup(DOOR_PIN, GPIO.OUT)
    GPIO.setup(DOOR_DETECT, GPIO.IN)
    GPIO.output(DOOR_PIN, False)

def cfgdb_init():
    pass
    
def sockinit():
    global clientsock
    #clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
def sensor_init():
    GPIO.setup(SENSOR_PIN, GPIO.IN)
    
def led_init():
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.setup(LED_1_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, False)
    GPIO.output(LED_1_PIN, False)
    
def writeio(dat):
    if dat == 0x00:
        GPIO.output(KEY_1, False)
        GPIO.output(KEY_2, False)
        GPIO.output(KEY_3, False)
    elif dat == 0x01:
        GPIO.output(KEY_1, False)
        GPIO.output(KEY_2, False)
        GPIO.output(KEY_3, True)
    elif dat == 0x02:
        GPIO.output(KEY_1, False)
        GPIO.output(KEY_2, True)
        GPIO.output(KEY_3, False)
    elif dat == 0x03:
        GPIO.output(KEY_1, False)
        GPIO.output(KEY_2, True)
        GPIO.output(KEY_3, True)
    elif dat == 0x04:
        GPIO.output(KEY_1, True)
        GPIO.output(KEY_2, False)
        GPIO.output(KEY_3, False)
    elif dat == 0x05:
        GPIO.output(KEY_1, True)
        GPIO.output(KEY_2, False)
        GPIO.output(KEY_3, True)
    elif dat == 0x06:
        GPIO.output(KEY_1, True)
        GPIO.output(KEY_2, True)
        GPIO.output(KEY_3, False)
    elif dat == 0x07:
        GPIO.output(KEY_1, True)
        GPIO.output(KEY_2, True)
        GPIO.output(KEY_3, True)
    else:
        pass
        
def readio():
    key_a = GPIO.input(KEY_A)
    key_b = GPIO.input(KEY_B)
    #print key_a, key_b
    if key_a == False and key_b == True:
        return 0x01
    elif key_a == True and key_b == False:
        return 0x02
    else:
        return 0x03

def getkeyboard():
    ret = None
    t = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06]
    for i in t:
        writeio(i)
        dat = readio()
        if (i,dat) == (0x00, 0x01):
            ret = KV1
        elif (i,dat) == (0x04, 0x01):
            ret = KV2
        elif (i,dat) == (0x02, 0x01):
            ret = KV3
        elif (i,dat) == (0x00, 0x02):
            ret = KV4
        elif (i,dat) == (0x04, 0x02):
            ret = KV5
        elif (i,dat) == (0x02, 0x02):
            ret = KV6
        elif (i,dat) == (0x01, 0x01):
            ret = KV7
        elif (i,dat) == (0x05, 0x01):
            ret = KV8
        elif (i,dat) == (0x03, 0x01):
            ret = KV9
        elif (i,dat) == (0x01, 0x02): # '*'
            ret = KV_DEL
        elif (i,dat) == (0x05, 0x02):
            ret = KV0
        elif (i,dat) == (0x03, 0x02): # '#'
            ret = KV_CONFIRM
        else:
            pass
    return ret

def do_scan(tick):
    global keyinput
    global keyscan_stage
    global key_t1
    global key_t2
    global keyscan_tick
    
    # 扫描 - 延时 - 再扫描（消抖）- 确认按下- 确认松开 = 一次完整按键动作
    if keyscan_stage == KEY_SCAN_0:
        key_t1 = getkeyboard()
        if key_t1:
            keyscan_stage = KEY_SCAN_1
            keyscan_tick = 0
    elif keyscan_stage == KEY_SCAN_1:
        keyscan_tick += tick
        if keyscan_tick >= KEYSCAN_DELAY:
            keyscan_stage = KEY_SCAN_2
    elif keyscan_stage == KEY_SCAN_2:
        key_t2 = getkeyboard()
        if key_t2 and key_t1 == key_t2:
            keyscan_stage = KEY_SCAN_3
        else:
            keyscan_stage = KEY_SCAN_0
    elif keyscan_stage == KEY_SCAN_3:
        if getkeyboard() == None:
            # 确认按键按下，播放按键音
            insert_q(sound_play_q, SOUND_CLICK)
            #print "t1:", time.time()
            if key_t1 == KV_DEL:
                # 如果是删除键（*），清除本次按键记录队列
                del keyinput[:]
                # 更新LCD显示
                cleanNotifyMsg()
            else:
                # 记录本次按键信息
                if len(keyinput) < (MAX_INPUT - 1):
                    keyinput.append(key_t1)
                    print keyinput
                elif key_t1 == KV_CONFIRM:
                    keyinput.append(key_t1)
                    print keyinput
            keyscan_stage = KEY_SCAN_0
            
           
def keyphase(tick):
    global keyinput
    if keyinput:
        #print keyinput
        #if keyinput[0] == KV_PRE and keyinput[-1] == KV_CONFIRM:
        if keyinput[-1] == KV_CONFIRM:  # 有确认键（#）按下
            passwd = ''.join(keyinput[0:-1])
            if True == cfgdb_check(TYPE_PASSWD, passwd):
                # 查询密码开门数据库成功
                # 播放密码失败声音
                insert_q(sound_play_q, SOUND_PASS)
                # 触发密码开门
                start_passwd_open(TYPE_PASSWD, passwd, int(time.time()))
                # 更新LCD显示
                setNotifyMsg(PASSWD_OPEN_SUCCESS_NOTIFY)
                print_ex("start_passwd_open")
            else:
                # 查询密码开门数据库失败
                # 播放密码开门失败声音
                insert_q(sound_play_q, SOUND_FAIL)
                setNotifyMsg(PASSWD_OPEN_FAIL_NOTIFY)
                print_ex("passwd_open_fail")

            del keyinput[:]
        else:
            msg = ""
            for i in range(0, len(keyinput)):
                msg += "*"
            # 更新LCD显示
            setNotifyMsg(msg)
        #elif keyinput[0] == KV_PRE and keyinput[-1] == KV_CALL:
        #    print_ex("get call input:%s" % ''.join(keyinput[1:-2]))
        #    del keyinput[:]
            
def keysan(tick):
    do_scan(tick)

def keyboard_poll(tick):
    keysan(tick)
    keyphase(tick)

def keyboard_init():
    GPIO.setup(KEY_3, GPIO.OUT)
    GPIO.setup(KEY_2, GPIO.OUT)
    GPIO.setup(KEY_1, GPIO.OUT)
    GPIO.setup(KEY_LED, GPIO.OUT)

    GPIO.setup(KEY_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(KEY_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def global_init():
    rf522.init()    # RF522模块初始化
    cfgdb_init()    # 数据库载入
    gpio_init()     # gpio初始化
    door_init()     # 门相关I/O初始化
    led_init()      # 显示灯相关I/O初始化
    lcd_init()      # 显示屏初始化
    sensor_init()   # 接近检测传感器初始化
    camera_init()   # 摄像头初始化
    sound_init()    # 声卡初始化
    record_pool_init()  # 开关门记录池初始化
    sockinit()          # 平台与门禁TCP连接初始化
    register_openers()  # urllib初始化（get/post请求使用）
    keyboard_init()     # 键盘初始化
    ble_init()          # 蓝牙初始化

WDAY = (u"日", u"一",u"二",u"三",u"四",u"五",u"六")

def create_screen():
    global screen
    global HEADER
    global DATETIME
    global GUIDE
    global CARD_OPEN
    global PASSWORD_OPEN
    global REMOTE_OPEN
    global NOTIFY
    global NOTIFYMSG
    global background

    screen.blit(background, (0,0))
    DATETIME_DISP["content"] = u"%d年%02d月%02d日 %02d时%02d分 星期%s" % (time.localtime().tm_year,
                                                   time.localtime().tm_mon, 
                                                   time.localtime().tm_mday, 
                                                   time.localtime().tm_hour,
                                                   time.localtime().tm_min,
                                                   WDAY[time.localtime().tm_wday])
    
    display_table = [HEADER_DISP, DATETIME_DISP, GUIDE_DISP, CARD_OPEN_DISP, PASSWORD_OPEN_DISP, REMOTE_OPEN_DISP, NOTIFY_DISP, NOTIFYMSG_DISP]
    
    for i in display_table:
        font = pygame.font.Font('/home/pi/dev/app/msyh.ttf', i["font"]) # 要显示的字体
        textSurfaceObj = font.render(i["content"], True, i["color"])    # 要显示的内容、颜色
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.x = i["pos"][0] # 显示的位置x
        textRectObj.y = i["pos"][1] # 显示的位置y
        screen.blit(textSurfaceObj, textRectObj)


def lcdflash():
    create_screen()         # 准备一屏数据
    pygame.display.update() # 更新至显示屏
        
def sensor_poll(tick):
    global sensor_detect_tick
    global sensor_detect_stage
    global sensor_status
    global open_status
    ENTER_EVENT = 1
    if sensor_detect_stage == SENSOR_DETECT_1:
        if ENTER_EVENT == GPIO.input(SENSOR_PIN) and False == sensor_status:
            # 检测到有人接近
            sensor_detect_stage = SENSOR_DELAY
            sensor_detect_tick = 0
    elif sensor_detect_stage == SENSOR_DELAY:
        # 延时消除抖动
        sensor_detect_tick += tick
        if sensor_detect_tick > SENSOR_DETECT_DELAY:
            sensor_detect_stage = SENSOR_DETECT_2
    elif sensor_detect_stage == SENSOR_DETECT_2:
        if ENTER_EVENT == GPIO.input(SENSOR_PIN):
            # 确认有人接近
            sensor_status = True
            open_status = False
            led_on()    # 开启摄像头灯照明
            print_ex('sensor detect')
        sensor_detect_stage = SENSOR_DETECT_1
        
def remoteOpenPoll(tick):
    global remoteopen_record_flag
    if remoteopen_record_flag == True:  # 远程开门标志
        remoteopen_record_flag = False
        setNotifyMsg(REMOTE_OPEN_SUCCESS_NOTIFY)  # 更新LCD显示远程开门成功
        start_remote_open(TYPE_REMOTE, None, int(time.time()))  # 触发远程开门
        
        
def bleOpenPoll(tick):
    global bleopen_record_flag
    if bleopen_record_flag == True: # 蓝牙开门标志
        bleopen_record_flag = False
        setNotifyMsg(BLE_OPEN_SUCCESS_NOTIFY)  # 更新LCD显示蓝牙开门成功
        start_ble_open()    # 触发蓝牙开门

old_msg = u""
msg_clean_tick = 0
MSG_CLEAN_TIMEOUT = 30000
msg_clean_stage = 0

def notifyMsgPoll(tick):
    global NOTIFYMSG_DISP
    global old_msg
    global msg_clean_tick
    global MSG_CLEAN_TIMEOUT
    global msg_clean_stage
    if NOTIFYMSG_DISP["content"]:
        if old_msg == NOTIFYMSG_DISP["content"]:
            msg_clean_tick += tick
            # LCD显示屏动态信息（目前为操作提示）显示一段时间（30s）后清除
            if msg_clean_tick >= MSG_CLEAN_TIMEOUT:
                cleanNotifyMsg()
                old_msg = u""
        else:
            old_msg = NOTIFYMSG_DISP["content"]
            msg_clean_tick = 0
    else:
        old_msg = u""
        msg_clean_tick = 0
       
        
def keepBleDiscoverable(tick):
    global bleWakeTick
    global BLE_WAKE_CYCLE
    bleWakeTick += tick
    if bleWakeTick >= BLE_WAKE_CYCLE:
        bleWakeTick = 0
        subprocess.Popen('echo "discoverable on \nquit" | bluetoothctl', shell=True)
        #print "keepBleDiscoverable"
        
        
def poll(tick):
    while True:
        remoteOpenPoll(tick)    # 处理远程开门请求
        bleOpenPoll(tick)       # 处理蓝牙开门请求
        cardDetectPoll(tick)    # 门禁卡检测
        cfgdb_checkPoll(tick)   # 数据库查询（刷卡后）
        doorCtrlPoll(tick)      # 执行开关门动作
        record_poll(tick)       # 拍照与视频录制逻辑
        phaseAckPoll(tick)      # 平台下发数据（命令）解析
        sensor_poll(tick)       # 接近传感器检测业务
        keyboard_poll(tick)     # 键盘扫描业务
        sound_poll(tick)        # 声音播放业务
        notifyMsgPoll(tick)     # 显示屏动态信息（操作提示）清除
        keepBleDiscoverable(tick) # 保持蓝牙可见
        time.sleep(tick/TIME_TICK_1S)

def commPoll(tick):
    while True:
        do_commPoll(tick)
        time.sleep(tick/TIME_TICK_1S)
        
def mainPoll(tick):
    while True:
        do_mainPoll(tick)
        time.sleep(tick/TIME_TICK_1S)
        
def sound_init():
    pygame.mixer.init(frequency=32000, size=-16, channels=2)
    pygame.mixer.music.set_volume(0.6)
       
# 刷屏线程 
def lcd_poll(tick):
    while True:
        lcdflash()
        time.sleep(tick/TIME_TICK_1S)
        
def sound_poll(tick):
    global sound_play_stage
    # 播放声音：载入音频文件，播放至结束
    if sound_play_stage == SOUND_PLAY_1:
        dat = get_q(sound_play_q)
        if dat:
            pygame.mixer.music.load("/home/pi/dev/app/%s.mp3" % dat) # 载入音频文件
            #print "t2:", time.time()
            pygame.mixer.music.play()   # 播放
            sound_play_stage = SOUND_PLAY_2
    elif sound_play_stage == SOUND_PLAY_2:
        if pygame.mixer.music.get_busy() != 1:  # 等待播放结束
            pygame.mixer.music.stop()       # 停止播放
            sound_play_stage = SOUND_PLAY_1

def send_cfgdb_updateRsut(current_seq, stat, cfgdb_key):
    dat = None
    
    print "send_cfgdb_updateRsut", stat, cfgdb_key
    
    t = list(cfgdb_key)
    for i in range(0, len(t)):
        t[i] = ord(t[i])
        
    print t
    
    if True == stat:
        dat = makeSyncBaseResult(current_seq, [0x0], t, getSendSeq())
    else:
        dat = makeSyncBaseResult(current_seq, [0x3], t, getSendSeq())
        
    syn_db_result_rsp_flag = False
    insert_q(tcp_send_q, dat)

def do_cfgdb_update(cfgdb_key):
    url = getFileUrl("db_get_url")  # 读出数据库更新链接
    device = getDevId() # 设备id
    textmod ={'device':''.join([chr(i) for i in device])}
    textmod = urllib.urlencode(textmod)
    req = urllib2.Request(url = '%s%s%s' % (url,'?',textmod))
    req.add_header('tpson_door', cfgdb_key) # http认证头

    try:
        res = urllib2.urlopen(req)   # 发出请求
    except:
       res = None

    print res
        
    if res:
        # 获得数据库文件，存储到本地
        res = res.read()
        with open(DB_PATH, 'w') as f:
            f.write(res)

        cx = sqlite3.connect(DB_PATH)
        cu = cx.cursor()
        cu.execute('Select * From tp_pass')
        for eachUser in cu.fetchall():
            print eachUser

        cu.execute('Select * From tp_server')
        for eachUser in cu.fetchall():
            print eachUser
        
        return True
    else:
        return False

def cfgdb_update_poll(tick):
    global cfgdbupdate_flag
    global cfgdb_key
    while True:
        if cfgdbupdate_flag == True:
            cfgdbupdate_flag = False    # 数据库更新标志已被触发
            current_seq = getSeq()
            cfgdb_key = getKey("dbkey")
            stat = do_cfgdb_update(cfgdb_key)   # 数据库更新操作
            send_cfgdb_updateRsut(current_seq, stat, cfgdb_key) # 回送数据库更新结果
        time.sleep(tick/TIME_TICK_1S)
        
FW_PATH = "/home/pi/dev/app/new.tar.gz"
        
def getFireware(name):
    print "getFireware"
    url = getFwUrl("fw_get_url")
    name_t = "%s.%s.%s.%s.tar.gz" % (name[0],name[1],name[2],name[3]*10+name[4])
    print name_t
    textmod ={'file':name_t}
    textmod = urllib.urlencode(textmod)
    print '%s%s%s' % (url,'?',textmod)
    req = urllib2.Request(url = '%s%s%s' % (url,'?',textmod))
    print getKey("fwkey")
    req.add_header('tpson_door', getKey("fwkey"))
    try:
        res = urllib2.urlopen(req)
    except:
        res = None

    if res:
        res = res.read()
        with open(FW_PATH, 'w') as f:
            print "get fw"
            f.write(res)
        return True
    else:
        return False
    

def sendFwUpdateStat(stat, msg):
    headers = {}
    headers['Content-Type'] = 'application/json; charset=utf-8'
    values = {}
    values["success"] = stat
    values["status"] = msg
    post_data = urllib.urlencode(values)
    j_data = json.dumps(values)
    req = urllib2.Request(getFwUrl("fw_stat_url"), j_data, headers)
    req.add_header('tpson_door', getKey("fwkey"))
    
    try:
        res = urllib2.urlopen(req)
    except:
        res = None
    if res:
        t = json.loads(res.read())
        print t
    
def fw_update_poll(tick):
    global fwupdate_flag
    global fw_key
    global fw_name
    while True:
        if fwupdate_flag == True:
            fwupdate_flag = False
            print fw_name
            if True == getFireware(fw_name):    # 固件更新请求，流程同数据库更新请求
                sendFwUpdateStat(True, u"success")
                print "do reset"
                os.system("reboot")
            else:
                sendFwUpdateStat(False, u"fail")
        time.sleep(tick/TIME_TICK_1S)
        
server_socket = None
ble_socket = None
ble_info = None

def ble_init():
    global server_socket
    server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_socket.bind(("",1))
    server_socket.listen(1)

BLE_ACCEPT_STAGE, BLE_RECV_STAGE = "BLE_ACCEPT_STAGE", "BLE_RECV_STAGE"
ble_accept_stage = BLE_ACCEPT_STAGE
        
def ble_recv():
    global server_socket
    global ble_socket
    global ble_info
    global ble_accept_stage
    receive = None
    if ble_accept_stage == BLE_ACCEPT_STAGE:
        ble_socket, ble_info = server_socket.accept()   # 等待蓝牙APP连接
        print str(ble_info[0]) + ' Connected!'
        ble_accept_stage = BLE_RECV_STAGE
    elif ble_accept_stage == BLE_RECV_STAGE:
        try:
            receive = ble_socket.recv(1024)  # 接收数据
            print '[' + str(ble_info) + ']' + receive
        except:
            ble_accept_stage = BLE_ACCEPT_STAGE
            receive = None
    return receive
    
def check_dat(dat):
    return True
    
def phaseBlePkg(dat):
    type, msgtype, msg = [], [], []
    type = dat[4:5]
    msgtype = dat[5:6]
    msg = dat[6:len(dat) - 4]
    return type, msgtype, msg
    
BLE_WRITE = [0x1] 
BLE_READ = [0x2]
BLE_SET_STATIC = [0x1]
BLE_SET_DYN = [0x2]
BLE_SET_DOORADDR = [0x3]
BLE_SET_ID = [0x4]
BLE_SET_FILEADDR = [0x5]
BLE_SET_FWADDR = [0x6]
BLE_SET_OPENDOOR = [0x7]
BLE_GET_INFO = [0x8]
BLE_GET_RUN_INFO = [0x9]
BLE_SUCCESS = [0x0]

def saveStaticIp(msg):
    with open(CFG_PATH, "r") as f:
        cfg_table = json.loads(f.read())
    cfg_table["ip1"], cfg_table["ip2"], cfg_table["ip3"], cfg_table["ip4"] = msg[0],msg[1],msg[2],msg[3]
    cfg_table["mask1"], cfg_table["mask2"], cfg_table["mask3"], cfg_table["mask4"] = msg[4],msg[5],msg[6],msg[7]
    cfg_table["gw1"], cfg_table["gw2"], cfg_table["gw3"], cfg_table["gw4"] = msg[8],msg[9],msg[10],msg[11]
    cfg_table["dns1"], cfg_table["dns2"], cfg_table["dns3"], cfg_table["dns4"] = msg[12],msg[13],msg[14],msg[15]
    cfg_table["mode"] = 2
    dat = json.dumps(cfg_table)
    with open(CFG_PATH, "w") as f:
        f.write(dat)

def saveDynIp():
    with open(CFG_PATH, "r") as f:
        cfg_table = json.loads(f.read())
    cfg_table["ip1"], cfg_table["ip2"], cfg_table["ip3"], cfg_table["ip4"] = 0,0,0,0
    cfg_table["mask1"], cfg_table["mask2"], cfg_table["mask3"], cfg_table["mask4"] = 0,0,0,0
    cfg_table["gw1"], cfg_table["gw2"], cfg_table["gw3"], cfg_table["gw4"] = 0,0,0,0
    cfg_table["dns1"], cfg_table["dns2"], cfg_table["dns3"], cfg_table["dns4"] = 0,0,0,0
    cfg_table["mode"] = 1
    dat = json.dumps(cfg_table)
    with open(CFG_PATH, "w") as f:
        f.write(dat)

def setStaticIP(msg):
    global static_cfg
    rsp = BLE_SUCCESS
    saveStaticIp(msg)
    file = static_cfg % (msg[0],msg[1],msg[2],msg[3],24,msg[8],msg[9],msg[10],msg[11],msg[12],msg[13],msg[14],msg[15])
    with open("/etc/dhcpcd.conf", 'w') as f:
        f.write(file)
    return rsp
    
def setDynIP():
    global dhcp_cfg
    rsp = BLE_SUCCESS
    saveDynIp()
    file = dhcp_cfg
    with open("/etc/dhcpcd.conf", 'w') as f:
        f.write(file)
    return rsp
    
def setDoorAddr(msg):
    rsp = BLE_SUCCESS
    setKV("door_url", ''.join([chr(i) for i in msg]))
    return rsp
    
def setDevId(msg):
    rsp = BLE_SUCCESS
    setKV("devid", ''.join([chr(i) for i in msg]))
    return rsp
    
def setFileAddr(msg):
    rsp = BLE_SUCCESS
    msg1 = msg[:8]
    msg2 = msg[8:]
    setKV("dbkey", ''.join([chr(i) for i in msg1]))
    setKV("file_url", ''.join([chr(i) for i in msg2]))
    return rsp
    
def setFwAddr(msg):
    rsp = BLE_SUCCESS
    msg1 = msg[:8]
    msg2 = msg[8:]
    setKV("fwkey", ''.join([chr(i) for i in msg1]))
    setKV("fw_url", ''.join([chr(i) for i in msg2]))
    return rsp
    
def setOpenDoor(msg):
    global bleopen_record_flag
    rsp = BLE_SUCCESS
    #start_ble_open()
    bleopen_record_flag = True
    return rsp
    
def phaseBleWrite(msgtype, msg):
    rsp = []
    if msgtype == BLE_SET_STATIC:   # 设置静态ip
        rsp = setStaticIP(msg)
        print "BLE_SET_STATIC"
    elif msgtype == BLE_SET_DYN:    # 设置动态ip
        rsp = setDynIP()
        print "BLE_SET_DYN"
    elif msgtype == BLE_SET_DOORADDR:    # 设置平台地址
        rsp = setDoorAddr(msg)
        print "BLE_SET_DOORADDR"
    elif msgtype == BLE_SET_ID: # 设置设备ID
        rsp = setDevId(msg)
        print "BLE_SET_ID"
    elif msgtype == BLE_SET_FILEADDR:    # 设置文件服务器地址与key
        rsp = setFileAddr(msg)
        print "BLE_SET_FILEADDR"
    elif msgtype == BLE_SET_FWADDR:     # 设置固件服务器地址与key
        rsp = setFwAddr(msg)
        print "BLE_SET_FWADDR"
    elif msgtype == BLE_SET_OPENDOOR:   # 蓝牙开门
        rsp = setOpenDoor(msg)
        print "BLE_SET_OPENDOOR"
    return rsp

ble_header = [0x24, 0x24]
ble_tail = [0x23, 0x23]

def makeRspPkg(wrtype, msgtype, rsp):
    # 读写信息类型1 信息体类型1 信息体n crc2
    dat = []
    dlen = 1 + 1 + len(rsp) + 2
    len_t = [0, 0]
    len_t[1] = dlen
    dat.extend(ble_header)
    dat.extend(len_t)
    dat.extend(wrtype)
    dat.extend(msgtype)
    dat.extend(rsp)
    crc = getCRC(dat[2:])
    dat.extend(crc)
    dat.extend(ble_tail)
    print "blersp", dat
    return array.array('B', dat).tostring()

def ble_getIpMaskGwDns():
    with open(CFG_PATH, "r") as f:
        cfg_table = json.loads(f.read())
    ip1, ip2, ip3, ip4 = cfg_table["ip1"], cfg_table["ip2"], cfg_table["ip3"], cfg_table["ip4"]
    m1, m2, m3, m4 = cfg_table["mask1"], cfg_table["mask2"], cfg_table["mask3"], cfg_table["mask4"]
    g1, g2, g3, g4 = cfg_table["gw1"], cfg_table["gw2"], cfg_table["gw3"], cfg_table["gw4"]
    d1, d2, d3, d4 = cfg_table["dns1"], cfg_table["dns2"], cfg_table["dns3"], cfg_table["dns4"]
    return [ip1,ip2,ip3,ip4,m1,m2,m3,m4,g1,g2,g3,g4,d1,d2,d3,d4]

def ble_getDevId():
    return getDevId()

def ble_getDoorUrl():
    addr = []
    doorurl = getKV("door_url")
    t = list(doorurl)
    addr.append(len(t))
    for i in t:
        addr.append(ord(i))
    #print_ex(addr)
    return addr

def ble_getfileUrl():
    addr = []
    fileurl = getKV("file_url")
    filekey = getKV("dbkey")
    t1 = list(fileurl)
    addr.append(len(t1))
    for i in t1:
        addr.append(ord(i))
    t2 = list(filekey)
    for i in t2:
        addr.append(ord(i))
    #print_ex(addr)
    return addr

def ble_getfwUrl():
    addr = []
    fwurl = getKV("fw_url")
    fwkey = getKV("fwkey")
    t1 = list(fwurl)
    addr.append(len(t1))
    for i in t1:
        addr.append(ord(i))
    t2 = list(fwkey)
    for i in t2:
        addr.append(ord(i))
    #print_ex(addr)
    return addr

def ble_getRunAddr():
    t = []
    mode = []
    ip_t = [0,0,0,0]
    netmask_t = [0,0,0,0]
    gw_t = [0,0,0,0]
    dns_t = [0,0,0,0]
    with open(CFG_PATH, "r") as f:
        cfg_table = json.loads(f.read())
    mode = [cfg_table["mode"]]
    try:
        addrs = netifaces.ifaddresses("eth0")
        ip = addrs[netifaces.AF_INET][0]['addr']
        mask = addrs[netifaces.AF_INET][0]['netmask']
        gw = netifaces.gateways()['default'][netifaces.AF_INET][0]
        ip_t[0] = int(ip.split('.')[0])
        ip_t[1] = int(ip.split('.')[1])
        ip_t[2] = int(ip.split('.')[2])
        ip_t[3] = int(ip.split('.')[3])
        netmask_t[0] = int(mask.split('.')[0])
        netmask_t[1] = int(mask.split('.')[1])
        netmask_t[2] = int(mask.split('.')[2])
        netmask_t[3] = int(mask.split('.')[3])
        gw_t[0] = int(gw.split('.')[0])
        gw_t[1] = int(gw.split('.')[1])
        gw_t[2] = int(gw.split('.')[2])
        gw_t[3] = int(gw.split('.')[3])
        dns_t = gw_t
    except:
        ip_t = [0, 0, 0, 0]
        netmask_t = [0, 0, 0, 0]
        gw_t = [0, 0, 0, 0]
        dns_t = [0, 0, 0, 0]
    t.extend(mode)
    t.extend(ip_t)
    t.extend(netmask_t)
    t.extend(gw_t)
    t.extend(dns_t)
    print ip_t, netmask_t, gw_t, dns_t
    return t

def phaseBleRead(msgtype):
    t = []
    if msgtype == BLE_GET_INFO: # 读取设备配置信息
        print "BLE_GET_INFO"
        t.extend(ble_getIpMaskGwDns())
        t.extend(ble_getDevId())
        t.extend(ble_getDoorUrl())
        t.extend(ble_getfileUrl())
        t.extend(ble_getfwUrl())
    elif msgtype == BLE_GET_RUN_INFO:   # 读取设备运行信息
        print "BLE_GET_RUN_INFO"
        t.extend(ble_getRunAddr())
        t.extend(timeconv(int(time.time())))
        t.extend(getFWversion())
    print "phaseBleRead", t
    return t

def bledataconv(dat):
    t = []
    dat_t = struct.unpack("%dc" % len(dat), dat)
    for i in range(0, len(dat)):
        t.append(six.byte2int(dat_t[i]))
    print "ble", t
    return t
    
def phaseBle(dat):
    ack = None
    if check_dat(dat) == False: # crc检查
        pass
    else:
        dat_t = bledataconv(dat)    # 数据转换
        type, msgtype, msg = phaseBlePkg(dat_t)
        if type == BLE_WRITE:   # 写类型命令
            rsp = phaseBleWrite(msgtype, msg)
            ack = makeRspPkg(BLE_WRITE, msgtype, rsp)
        elif type == BLE_READ:  # 读类型命令
            rsp = phaseBleRead(msgtype)
            ack = makeRspPkg(BLE_READ, msgtype, rsp)
    return ack

def ble_send(rsp):
    global ble_socket
    ble_socket.send(rsp)

def ble_poll(tick):
    while True:
        dat = ble_recv()
        if dat:
             # 接收到数据，解析
            rsp = phaseBle(dat)
            if rsp:
                # 发送应答数据
                ble_send(rsp)
        time.sleep(tick/TIME_TICK_1S)
    
    
if __name__ == '__main__':
    global_init()   # 全局初始化

    threads = []
    
    # 轮询任务线程
    t1 = threading.Thread(target=poll, args=(TICK_POLL,))
    threads.append(t1)

    # TCP数据接收线程
    t2 = threading.Thread(target=comm_recv, args=(TICK_POLL,))
    threads.append(t2)

    # TCP数据发送
    t3 = threading.Thread(target=comm_send, args=(TICK_POLL,))
    threads.append(t3)

    # 数据主动上送线程（心跳、诊断、记录）
    t4 = threading.Thread(target=mainPoll, args=(TICK_POLL,))
    threads.append(t4)
    
    # 刷屏线程
    t5 = threading.Thread(target=lcd_poll, args=(LCD_FLASH_CYCLE,))
    threads.append(t5)
    
    # 数据库更新线程
    t6 = threading.Thread(target=cfgdb_update_poll, args=(TICK_POLL,))
    threads.append(t6)
    
    # 固件更新线程
    t7 = threading.Thread(target=fw_update_poll, args=(TICK_POLL,))
    threads.append(t7)
    
    # 蓝牙通信线程
    t8 = threading.Thread(target=ble_poll, args=(TICK_POLL,))
    threads.append(t8)

    for t in threads:
        t.setDaemon(True)
        t.start()
        
    for t in threads:
        t.join()

    

    

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
