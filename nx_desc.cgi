#
#  IRiS nX link descriptor
#  -----------------------
#  Copyright(C)2000-2001. NvyU. (20010211 release)
#	   E-MAIL	: nvyu@hitel.net
#	   HOMEPAGE : http://nvyu.net/
#

%extension
image:jpg,gif,png,jpeg
#
# flash:swf,fla ... 라든가를 추가하신다면...
# 저 아래에도 %flash 라는 부분을 넣으셔서 그것에 대한 링크를.!
# nx_desc.cgi 파일에 대한 자세한 내용은 upgrade.txt 파일을 읽어주세요.
#
#######################################################

#
# 이전 버전의 로그들은 0번으로 선언되어 있는 스타일의 영향을 받습니다.
# %번호:이름

%0:center
%image
<div align=center><img src="<-!->" border=0 vspace=3></div>

%extra
<a href="<-!->"><-o-></a>



%1:left
%image
<img src="<-!->" border=0 vspace=3 align=left>

%extra
<a href="<-!->"><-o-></a>



%2:right

%image
<img src="<-!->" align=right border=0 vspace=3>

%extra
<div align=right><a href="<-!->"><-o-></a></div>



# %3 .. %4... 는 직접 ... -_-;