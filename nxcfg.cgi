#
#  IRiS nX configuration template
#  ------------------------------
#
#  Copyright(C)2000-2001. NvyU. (20001119 release)
#	   E-MAIL	: nvyu@hitel.net
#	   HOMEPAGE : http://nvyu.net
#
#  안내 사항.
#  - 이 스크립트는 공개로 제공됩니다. 이 스크립트를 사용할 경우에 생길 수 있는
#	 손해 등에 대해서 제작자는 일체 책임을 지지 않습니다.
#  - 설치 등과 관련된 질문은 제작자의 홈페이지의 QNA 보드에서 문의하실 수 있습니다.
#  - 원하시는 추가 기능이 있으실 경우에는 리퀘스트 해주시면 감사하겠습니다.
#
#################################################################################

$email = 'nX@whatmean.it.is';    # email 주소 

$password = "1234";                   # 패스워드

##################################################################################


$nx_main = "nx_main.htm";  # 메인 HTML
$nx_view = "nx_view.htm";  # 보기 템플릿
$nx_repl = "nx_reply.htm"; # 레스 템플릿

$nx_resf = "nx_resf.htm";  # 레스 폼 페이지
$nx_rview = "nx_viewr.htm";
$nx_rrply = "nx_resr.htm";

$nx_desc = "nx_desc.cgi";

$data_url = "data/";                    # 데이터 URL
$data_dir = "data/";                  # 데이터 디렉토리
$nx_log = "irisnx.log";       # 로그 파일

$backup_dir = "backup/";               # 백업 디렉토리
$backup_log = "backup.log"; # 백업 로그명


###############################################################################

$url = qq|<a href="<-!->" target="_blank"><-!-></a>|; 
                                        # url 표시 방법 : <-!->는 URL 주소를 반환합니다.

$img_link = qq|<img src="<-!->" align=right border=0 vspace=3>|;
										# 데이터 파일로 이미지가 올라왔을 때 표시 방법

$etc_link = qq|<a href="<-!->"><-o-></a>|;
                                        # 데이터 파일로 이미지 파일이 아닌 파일이 올라왔을때
										# 표시 방법.

										# <-!->에는 URL이 포함된 이미지 파일명이 반환됩니다.
										# <-o->에는 이미지 파일명만 반환됩니다.

$reply_link = qq|<a href="<-!->">[REPLY]</a>|;
                                        # reply 링크 태그.

################################################################################


$prev_link = qq|<a href="<-!->">[PREV]</a>|;            
$next_link = qq|<a href="<-!->">[NEXT]</a>|;
                                        # 이전, 다음페이지 표시 태그
$no_prev = qq|[FIRST]|;
$no_next = qq|[LAST]|;
										# 첫페이지, 마지막페이지일 경우 표시 태그

###############################################################################

$res_move_top = 0;                      # 레스달린 글을 가장 위로 올릴까요?
										# 0 - 올리지 않는다.
										# 1 - 올린다

$page = 15;                           # 한 페이지당 표시될 게시물 수                              
$style = 0;          # 페이지바 표시 방법 0 - [1]...[48][49][50][51][52]...[99]
                     #                    1 - [48][49][50][51][52]


$max = 500;                             # 한 로그당 최대 게시물 수 (메인 아티클 기준)

$lockfile = "$data_dir/irisnx.lock";      # LOCK 파일 경로
$lock = 2;                                # 0 - no use, 1 = symlink, 2 = open


###########################################


$must{'name'} = 2; 
$must{'email'} = 0; 
$must{'url'} = 0;
$must{'title'} = 0;
$must{'comment'} = 2;
$must{'file'} = 0;
# 0 - 작성하지 않아도 좋아요, 1 - 일반게시물작성시 꼭 써야 해요, 
# 2 - 답글 작성시 꼭 써야 해요, 3 - 어쨌거나 써야 해요 - -;;


# 0 - 아무 파일이나 가능해요, 1 - 등록된 파일만 가능해요.
$must_allowed = 0; 

$art_reverse = 0; # 메인 아티클 반전처리.
$res_reverse = 0;

$art_register = 1;       # 메인 아티클 작성 허용 여부
$res_register = 0;       # 레스 작성 허용 여부
# 0 - 누구나, 1 - 관리자만, 


# HTML 사용 여부, 0 - 사용불능, 1 - 관리자만 사용가능, 2 - 누구나 사용 허용
$html_use = 1;
$autolink = 1;    # URL 자동 링크 허용 여부

$outsidelink = 1; # FILE 필드에 URL 입력으로 불러오기 허용 여부 0 - 불능, 1 - 관리자만 가능, 2 - 누구나 가능

# 제목이 없을 때의 기본 제목
$default_title = "";

$gradcolor  = "#000000";
$gradcolor2 = "#555555";


# 이미지 업로드 제한 크기 (kb 단위, 0은 제한 안함)
$img_limit = 100;


# 쿠키 아이디. (수정 불필요)
$cookie_id = 'nx';

1;