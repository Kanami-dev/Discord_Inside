import json
import time
import requests

from json.decoder import JSONDecodeError
from pypresence import Presence
from flask import Flask, request
from urllib.parse import unquote

client_id = '794449494585638922'

rpc = Presence(client_id)
app = Flask(__name__)


def dccon_name(dccon_id: int):
    Cookie = {'X-Requested-With': 'XMLHttpRequest'}
    url = 'https://dccon.dcinside.com/index/package_detail'
    r = requests.get(url, headers=Cookie)
    data = {'ci_t': r.cookies['ci_c'], 'package_idx': dccon_id}
    return requests.post(url, headers=Cookie, data=data).json()['info']['title']


def dcurl(title, url):
	#[디시콘샵]===========
	if url.startswith('https://dccon.dcinside.com'):
		details = '디시콘샵'
		state = '디시콘샵'
	if url.startswith('https://dccon.dcinside.com/#'):
		try:
			dccon_id = int(url.replace('https://dccon.dcinside.com/#', ''))
			details = '디시콘샵'
			state = dccon_name(dccon_id)
		except ValueError:
			pass

	#[디시 이벤트]===========
	if url.startswith('https://event.dcinside.com'):
		details = '디시인사이드'
		state = '이벤트'
		if url.startswith('https://event.dcinside.com/view'):
			details = '디시인사이드 이벤트'
			state = title
	
	#[디시 로그인]===========
	if url.startswith('https://dcid.dcinside.com/join/login.php'):
		details = '디시인사이드'
		state = '로그인'
	if url.startswith('https://dcid.dcinside.com/join_new/member_find_id.php'):
		details = '디시인사이드 로그인'
		state = '아이디 찾기'
	if url.startswith('https://dcid.dcinside.com/join_new/member_find_pw.php'):
		details = '디시인사이드 로그인'
		state = '비밀번호 재설정'
	
	#[디시 갤로그]===========
	if url.startswith('https://gallog.dcinside.com/'):
		details = '갤로그'
		state = url.split('/')[-1]
		if url.endswith('/posting'):
			details = '갤로그 게시글'
			state = url.split('/')[-2]
		if url.endswith('/comment'):
			details = '갤로그 댓글'
			state = url.split('/')[-2]
		if url.endswith('/scrap'):
			details = '갤로그 스크랩'
			state = url.split('/')[-2]
		if url.endswith('/guestbook'):
			details = '갤로그 방명록'
			state = url.split('/')[-2]

	#[디시 게임]===========
	if url.startswith('https://h5.dcinside.com/'):
		details = '디시게임'
		if url.endswith('game/main'):
			state = '디시게임'
		if url.endswith('item/shop'):
			state = '뽑기/응모'
		if url.endswith('attendance'):
			state = '출석체크'
		else:
			state = '디시게임'

	#[디시 디시위키]===========
	if url.startswith('https://wiki.dcinside.com/wiki/'):
		details = '디시위키'
		state = unquote(url.replace('https://wiki.dcinside.com/wiki/', '')).split('#.')[0]

	#[디시 메인]===========
	if url.startswith('https://www.dcinside.com'):
		details = '디시인사이드'
		state = '메인'

	#[디시 갤러리]===========
	if url.startswith('https://gall.dcinside.com'):
		details = '디시인사이드'
		state = '갤러리'
		if url.startswith('https://gall.dcinside.com/board/lists'):
			details = title
			if url.endswith('&exception_mode=recommend'):
				state = '개념글'
			elif url.endswith('&exception_mode=notice'):
				state = '공지'
			else:
				state = '전체글'

	#[디시 마이너 갤러리]===========
	if url.startswith('https://gall.dcinside.com/m'):
		details = '디시인사이드'
		state = '마이너 갤러리'
	if url.startswith('https://gall.dcinside.com/mgallery/board/lists'):
		details = title[:-3] + '마이너 갤러리'
		if url.endswith('&exception_mode=recommend'):
			state = '개념글'
		elif url.endswith('&exception_mode=notice'):
			state = '공지'
		else:
			state = '전체글'

	#[디시 미니 갤러리]===========
	if url.startswith('https://gall.dcinside.com/n'):
		details = '디시인사이드'
		state = '미니 갤러리'
	if url.startswith('https://gall.dcinside.com/mini/board/lists'):
		details = title[:-3] + '미니 갤러리'
		if url.endswith('&exception_mode=recommend'):
			state = '개념글'
		elif url.endswith('&exception_mode=notice'):
			state = '공지'
		else:
			state = '전체글'

	#[디시 게시글]===========
	gall = title.split(' - ')[-1]
	if url.startswith('https://gall.dcinside.com/board/view'):
		details = gall
		state = title.replace(gall, '')[:-3]
	elif url.startswith('https://gall.dcinside.com/mgallery/board/view'):
		details = gall[:-3] + '마이너 갤러리'
		state = title.replace(gall, '')[:-3]
	elif url.startswith('https://gall.dcinside.com/mini/board/view'):
		details = gall[:-3] + '미니 갤러리'
		state = title.replace(gall, '')[:-3]

	return details, state


@app.route('/', methods=['POST'])
def index():
	try:
		body = json.loads(request.data)
	except JSONDecodeError:
		rpc.clear()
		return ''

	if body['action'] == 'set':
		details, state = dcurl(body['title'], body['url'])
		rpc.update(
			state = state[:128].strip(),
			details = details[:128].strip(),
			start = time.time(),
			large_image = 'dclogo',
			buttons = [{"label": "바로가기", "url": body['url']}]
			)
	else:
		rpc.clear()
	return ''


rpc.connect()
app.run('localhost', 27328, False)
