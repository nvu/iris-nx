#!/usr/bin/perl	

$soft = "IRiS nX"; $ver = "1.3";
#
#  IRiS nX
#  -------
#  Copyright(C)2000-2001. NvyU. (20010211 release)
#	   E-MAIL	: nvyu@hitel.net
#	   HOMEPAGE : http://nvyu.net/
#
#  안내 사항.
#  - 이 스크립트는 공개로 제공됩니다. 이 스크립트를 사용할 경우에 생길 수 있는
#	 손해 등에 대해서 제작자는 일체 책임을 지지 않습니다.
#  - 원하시는 추가 기능이 있으실 경우에는 리퀘스트 해주시면 감사하겠습니다.
#  - 저작권 정보는 수정하지 말아주세요.
#
#

	require 'nxcfg.cgi';
	
	umask(000);

	$env = $ENV{'SCRIPT_NAME'}; @env = split(/\//, $env);
	$StartClock = (times)[0];

	$data_dir .= "/" if ($data_dir !~ /\/$/);
	$data_url .= "/" if ($data_url !~ /\/$/);
	$backup_dir .= "/" if ($backup_dir !~ /\/$/);
	$nx_log = $data_dir . $nx_log;  
	$backup_log = $backup_dir . $backup_log;

	$gradcolor =~ s/#//g; $gradcolor2 =~ s/#//g;

	$tmpfile = $data_dir . "haruka";

	$angels = 10;
	@sister_princess = ('num', 'sn', 'name', 'email', 'url', 'time', 'comment', 'filename', 'title', 'style', '');

	&get_form; &get_cookie; 

	$admin = 1 if ($COOKIE{'ren'} eq $password && $F{'m'} ne 'leaf');

	$scr = $ENV{'SCRIPT_NAME'};	$scr =~ s/(~|%7E)//g; 
	$ref = $ENV{'HTTP_REFERER'}; $ref =~ s/(~|%7E)//g;
	&msg_error("setting", "it's iris nX! please rename installed directory.") if ($env[$#env-1] =~ /(pury|up|asq)/i);
	&msg_error("submit", "illegal referer") if ($F{'m'} =~ /(reg|res|ers|emt|aru|k|miho|mariko)/ && $scr ne '' && $ref !~ /$scr/);

	unlink($tmpfile) if ($F{'m'} eq 'dwn' && $admin == 1);
	if ($F{'m'} eq 'k' && $admin == 1 && $F{'f'} ne 'irisnx.log' && $F{'f'} ne 'index.htm') { unlink("$data_dir$F{'f'}"); $F{'m'} = 'aru'; }

	&cvt_html; 


	if ($F{'m'} eq 'reg') {	
		if ($art_register != 1 or ($art_register == 1 && $admin == 1)) {
			if ($F{'anum'} eq '') {
				&lock;
				@TOTLOG = &get_file($nx_log); $F{'num'} = $TOTLOG[0] + 0; shift(@TOTLOG);
				foreach (0 .. 5) { @TMP = split(/\|/, $TOTLOG[$_]); &msg_error("submit","resubmitted?") if ($TMP[2] eq $F{'name'} && $TMP[6] eq $F{'comment'}); }
				$F{'num'} += 1; 
				$F{'title'} = $default_title if ($F{'title'} eq '');
				$F{'time'} = get_vtime(time); $F{'sn'} = "";
				if ($F{'file.name'} =~ /^(http|ftp|telnet):\/\// && (($outsidelink == 1 && $admin == 1) or $outsidelink == 2)) { $F{'filename'} = $F{'file.name'}; }
				else { $F{'filename'} = &sav_file if ($F{'file'} ne ''); }
				&makeup;
				unshift(@TOTLOG, $MSG);
				@TOTLOG = &log_limit(@TOTLOG);
				&put_file($nx_log, ("$F{'num'}\n", @TOTLOG));
				&unlock;
				&put_cookie($F{'name'}, $F{'email'},$F{'url'});
				$F{'m'} = 'rdm';
			} else {
				($F{'num'}, $F{'sn'}) = split(/_/, $F{'anum'});
				$F{'time'} = &spt_date($F{'date'}, $F{'time'}, $F{'week'}); 
				&lock;
				@TOTLOG = &get_file($nx_log); $num = $TOTLOG[0] + 0; shift(@TOTLOG);
				foreach $LOG (@TOTLOG) {
					@TMP = split(/\|/, $LOG);
					if ($TMP[0] == $F{'num'} && $TMP[1] == $F{'sn'}) {
						&makeup;
						push(@NEWLOG, $MSG);
					}
					else { push(@NEWLOG, $LOG); }
				}
				&put_file($nx_log, ("$num\n", @NEWLOG));
				@TOTLOG = @NEWLOG; undef(@NEWLOG);
				&unlock;
				$F{'m'} = '';
			}
		} else { $F{'m'} = ''; }
	} 
	elsif ($F{'m'} eq 'res') {
		if ($res_register != 1 or ($res_register == 1 && $admin == 1)) {
			undef(@ADDLOG); undef(@NEWLOG); 
			if ($F{'file.name'} =~ /^(http|ftp|telnet):\/\// && (($outsidelink == 1 && $admin == 1) or $outsidelink == 2)) { $F{'filename'} = $F{'file.name'}; }
			else { $F{'filename'} = &sav_file if ($F{'file'} ne ''); }
			&lock;
			@TOTLOG = &get_file($nx_log); $num = $TOTLOG[0] + 0; shift(@TOTLOG);
			foreach (@TOTLOG) { @TMP = split(/\|/, $_); &msg_error("reply", "resubmitted?") if ($TMP[2] eq $F{'name'} && $TMP[6] eq $F{'comment'}); }
			foreach $LOG (@TOTLOG) {
				@TMP = split(/\|/, $LOG);
				if ($TMP[0] == $F{'n'}) {
					if ($already != 1) {
						$F{'num'} = $F{'n'};
						$F{'sn'} = $TMP[1] + 1;
						$F{'title'} = $default_title if ($F{'title'} eq '');
						$F{'time'} = &get_vtime(time);
						&makeup;
						if ($res_move_top != 1) { push(@NEWLOG, $MSG); }
						else { push(@ADDLOG, $MSG); }
						$already = 1;
					}
					if ($res_move_top != 1) { push(@NEWLOG, $LOG); }
					else { push(@ADDLOG, $LOG); }
				} 
				else { push(@NEWLOG, $LOG); }
			}
			unshift(@NEWLOG, @ADDLOG);
			@NEWLOG = &log_limit(@NEWLOG);
			&put_file($nx_log, ("$num\n", @NEWLOG));
			&unlock;
			@TOTLOG = @NEWLOG;
			&put_cookie($F{'name'}, $F{'email'},$F{'url'});
		}
		$F{'m'} = ($F{'r'} ne '') ? 'rfm' : '';				
		$F{'p'} = 1 if ($res_move_top == 1 && $admin == 0);
	} 
	elsif ($F{'m'} eq 'miho' && $admin == 1) {
		if ($F{'file.name'} =~ /^(http|ftp|telnet):\/\// && (($outsidelink == 1 && $admin == 1) or $outsidelink == 2)) { $F{'filename'} = $F{'file.name'}; }
		else { $F{'filename'} = &sav_file if ($F{'file'} ne ''); }
		if ($F{'mizuho'} ne '') {
			($F{'num'}, $F{'sn'}) = split(/_/, $F{'mizuho'});
			$fname = $F{'filename'};
			&lock;
			@TOTLOG = &get_file($nx_log); $num = $TOTLOG[0] + 0; shift(@TOTLOG);
			foreach $LOG (@TOTLOG) {
				@TMP = split(/\|/, $LOG);
				if ($TMP[0] == $F{'num'} && $TMP[1] == $F{'sn'}) {
					unlink("$data_dir$TMP[7]") if ($TMP[7] !~ /^(http|ftp|telnet):\/\//);
					&moon_crystal; $F{'filename'} = $fname; &makeup; push(@NEWLOG, $MSG);
				}
				else { push(@NEWLOG, $LOG); }
			}
			&put_file($nx_log, ("$num\n", @NEWLOG));
			@TOTLOG = @NEWLOG; undef(@NEWLOG);
			&unlock;
			$F{'m'} = 'aru';
		}
		else { 
			if ($F{'filename'} =~ /^(http|ftp|telnet):\/\//) { &msg_error("file upload", "Why you are trying to upload URL?"); } 
			elsif ($F{'filename'} eq '') { &msg_error("File upload", "File not found."); } 
			else { 
				if ($F{'filename'} =~ /^(http|ftp|telnet):\/\//) { $CP = $F{'filename'}; } else { $CP = qq|$data_url$F{'filename'}|; }
				&msg_error("File upload", qq|<a href="$CP" target="_blank">$F{'filename'}</A> uploaded.|, "aru"); 
			}
		}
	}
	else {
		if ($F{'m'} eq 'elf' or $F{'m'} eq 'login') { 
			if ($F{'pwd'} ne $password) {		
				$dmi = qq|<p><form method=post action="irisnx.cgi"><input type=hidden name="m" value="elf"><table border=1 cellspacing=0 cellpadding=0 bgcolor="#ffeeee" style="filter:alpha(opacity=70)"><tr><td><table width=100% cellspacing=0 cellpadding=2 border=0>|;
				$dmi .= qq|<tr><td colspan=3 align=center><font size=2 color="black">로그인을 위해 패스워드를 입력해주세요. <a href="irisnx.cgi?m=leaf"><font color=red>(LOGOUT)</font></a></font></td></tr>|;
				$dmi .= qq|<tr><td align=center><font size=2 color="black">ADMIN PASSWORD</font></td><td align=center><input type=password name=pwd size=10></td><td align=center><input type=submit value="carrot!"></td></tr>|;
			}
			else { print "Set-Cookie: ren=$F{'pwd'}\n"; $admin = 1; }
		} 
		elsif ($F{'m'} eq 'leaf') { print "Set-Cookie: ren=\n"; $admin = 0; }
		&lock; @TOTLOG = &get_file($nx_log); $num = $TOTLOG[0] + 0; shift(@TOTLOG);
		if ($F{'m'} eq 'manami' && $admin == 1) {
			undef(@NEWLOG);
			foreach $LOG (@TOTLOG) {
				@TMP = split(/\|/, $LOG);
				if (length $miko{"$TMP[0]_"} == 13 || length $miko{"$TMP[0]_$TMP[1]"} == 13) { 
					if ($TMP[7] ne '') { 
						if ($F{'mv'} eq 'on') {
							$filename = &get_filename($backup_dir, $TMP[7]);
							rename("$data_dir$TMP[7]", "$backup_dir$filename") if ($TMP[7] !~ /^(http|ftp|telnet):\/\//);
						} 
						else { unlink("$data_dir$TMP[7]") if ($TMP[7] !~ /^(http|ftp|telnet):\/\//);}
					}
				}
				else { push(@NEWLOG, $LOG); }
				
			}
			&put_file($nx_log, ("$num\n", @NEWLOG));
			@TOTLOG = @NEWLOG;
		}
		&unlock;
	}

	if ($admin == 1) {
		$nmsg = qq|/ <a href="irisnx.cgi?m=dwn&p=$F{'p'}"><font color=red>경고 메시지 제거</font></a>| if (-e $tmpfile);
		$eddt = "게시물 삭제 모드" if ($F{'m'} eq 'ers');
		$eddt = "게시물 수정 모드" if ($F{'m'} eq 'edt');
		$eddt = "파일 관리 모드" if ($F{'m'} eq 'aru');


		$dmi = qq|<p><form method=post action="irisnx.cgi"><input type=hidden name="m" value="elf"><table border=0 cellspacing=0 cellpadding=0><tr><td><table width=100% cellspacing=0 cellpadding=2 border=1 bordercolor="#000000" bgcolor="#ffeeee" style="filter:alpha(opacity=80)">| if ($dmi eq '');
		$dmi .= qq|<tr><td align=center colspan=3><font size=2><a href="irisnx.cgi?p=$F{'p'}">게시물 보기</a> / <a href="irisnx.cgi?m=edt&p=$F{'p'}"><font color=red>게시물 편집</font></a> / <a href="irisnx.cgi?m=ers&p=$F{'p'}"><font color=red>게시물 삭제</font></a> / <a href="irisnx.cgi?m=aru">파일 관리</a> / <a href="irisnx.cgi?m=leaf"><font color=red>로그아웃</font></a> $nmsg</font></td></tr>|;
	}

	$dmi .= qq|</table></td></tr></table></form><p>| if ($dmi ne '');
	$dmi .= qq|<p><font size=3>- 계정 공간이 부족합니다 - <br>관리자가 문제를 해결할 때까지 <b>게시물 투고를 자제해주시기 바랍니다.</b></font><p>| if (-e $tmpfile);
	if ($F{'m'} ne 'rfm') { 
		@main = &get_file($nx_main); 
		@view = &get_file($nx_view);
		@repl = &get_file($nx_repl);
	}  
	else { 
		@main = &get_file($nx_resf);
		if (-f $nx_rview) { @view = &get_file($nx_rview); } else { @view = &get_file($nx_view); }
		if (-f $nx_rrply) { @repl = &get_file($nx_rrply); } else { @repl = &get_file($nx_repl); }
	}

	undef($repl); foreach $_ (@repl) { $repl .= $_; }

	foreach $LOG (@TOTLOG) {
		($num, $sgn) = split(/\|/, $LOG);
		if ($sgn eq '') { push(@LOG, $LOG); }
		else { $TL{$num}++; push(@RES, $LOG); }
	}

	@LOG = reverse @LOG if $art_reverse == 1;
	@RES = reverse @RES if $res_reverse == 1;

	$F{'p'} = int($F{'p'}); $F{'p'} = 1 if ($F{'p'} < 1);
	$V{'tlog'} = $#LOG + 1; $V{'tres'} = $#RES + 1; $V{'trate'} = 0; $V{'trate'} = int(($#RES + 1) / ($#LOG + 1) * 10 ) / 10 if $#LOG + 1 != 0 ;
	$extra = 1 if (($V{'tlog'} % $page) != 0);
	$V{'totp'} = int($V{'tlog'} / $page) + $extra;
	$F{'p'} = $V{'totp'} if ($F{'p'} > $V{'totp'} || ($F{'m'} eq 'rdm' && $art_reverse == 1)); $V{'page'} = $F{'p'};

	if ($F{'m'} eq 'rfm') {
		$tmp = $p_prev = $p_next = 0; 
		foreach (@LOG) {
			@_ = split(/\|/);
			if ($F{'n'} == $_[0] && $tmp == 0) { $p_prev = $ppp; $tmp += 1; }
			elsif ($tmp == 1) { $p_next = $_[0]; last; }
			else { $ppp = $_[0]; }
		}
		if ($p_prev > 0) { $V{'prev'} = $prev_link; $V{'prev'} =~ s/<-!->/irisnx.cgi?m=$F{'m'}&p=$F{'p'}&n=$p_prev/i; } else { $V{'prev'} = $no_prev; }
		if ($p_next != 0) { $V{'next'} = $next_link; $V{'next'} =~ s/<-!->/irisnx.cgi?m=$F{'m'}&p=$F{'p'}&n=$p_next/i;} else { $V{'next'} = $no_next; }
	}
	else {
		foreach (1 .. ($F{'p'} - 1) * $page) { shift(@LOG); }; 
		$#LOG = $page - 1 if ($#LOG >= $page); 
		$p_prev = $F{'p'} - 1; $p_next = $F{'p'} + 1;
		if ($p_prev > 0) { $V{'prev'} = $prev_link; $V{'prev'} =~ s/<-!->/irisnx.cgi?m=$F{'m'}&p=$p_prev/i; } else { $V{'prev'} = $no_prev; }
		if ($p_next < $V{'totp'} + 1) { $V{'next'} = $next_link; $V{'next'} =~ s/<-!->/irisnx.cgi?m=$F{'m'}&p=$p_next/i;} else { $V{'next'} = $no_next; }
		$V{'page_bar'} = &get_pagebar($V{'page'}, $V{'totp'}, $style);
	}

	&header;
	if ($admin == 1) {
		if ($F{'m'} eq 'mariko') {
			&move_yourbody;
			foreach $LOG (@TOTLOG) {
				@TMP = split(/\|/, $LOG);
				if (length $miko{"$TMP[0]_$TMP[1]"} == 13) {
					($E{'no'}, $E{'sno'}, $E{'name'}, $E{'email'}, $E{'url'}, $E{'time'}, $E{'comment'}, $E{'filename'}, $E{'title'}, $E{'style'}) =  split(/\|/, $LOG);
					$E{'comment'} =~ s/<br>|<BR>/\n/g;
					$E{'comment'} =~ s/</&lt;/g;
					$E{'comment'} =~ s/>/&gt;/g;
					%A = &get_time($E{'time'});
					$NN = $E{'no'}; $NN .= qq| - $E{'sno'}| if ($E{'sno'} ne '');
					$VD = qq|$A{'yyyy'}/$A{'mm'}/$A{'dd'}|; $VT = qq|$A{'ho'}:$A{'mi'}:$A{'se'}|;
					@week = (Sun,Mon,Tue,Wed,Thu,Fri,Sat); $VP = '';
					foreach (0 .. 6) {
						if ($_ == $A{'week_p'}) { $VKT = ' selected'; } else { $VKT = ''; }
						$VP .= qq|<OPTION VALUE="$_"$VKT>$week[$_]|;
					}
					&honoka_sawatari;
					$dmi .= qq|<font size=2>게시물 편집 모드입니다.<br>파일 수정 전송은 파일 관리 메뉴를 사용해주세요.<br>|;
					print qq|<html><head></head><body><div align=center>$dmi|;
					print qq|<form method=post action="irisnx.cgi"><input type=hidden name="m" value="reg"><table border=1 cellspacing=0 cellpadding=1>\n|;
					print qq|<input type=hidden name="anum" value="$E{'no'}_$E{'sno'}"><input type=hidden name="filename" value="$E{'filename'}">\n|;
					print qq|<tr><td rowspan=3 align=center><b>$NN</b></td><td><font size=2>NAME</font></td><td colspan=2><input type=text name="name" value="$E{'name'}" size=20><td><font size=2>EMAIL</font></td><td><input type=text name="email" value="$E{'email'}" size=12></td><td><font size=2>URL</font></td><td><input type=text name="url" value="$E{'url'}" size=12></td></tr>\n|;
					print qq|<tr><td><font size=2>DATE</font></td><td><input type=text name="date" value="$VD" size=12></td><td><select name="week">$VP</select></td><td><font size=2>TIME</font></td><td><input type=text name="time" value="$VT" size=12></td><td><font size=2>ATTACH</font></td><td><input type=text name="filename" value="$E{'filename'}" size=12></td></tr>\n|;
					print qq|<tr><td><font size=2>TITLE</font></td><td colspan=6><input type=text name="title" value="$E{'title'}" size=75></td></tr>\n|;
					print qq|<tr><td align=center colspan=8><textarea name="comment" rows=15 cols=75>$E{'comment'}</textarea></td></tr>\n|;
					print qq|<tr><td colspan=2><font size=2>ATTACH STYLE</font></td><td><select name="style">$V{'style_list'}</select></td><td align=right colspan=5><input type=submit value=" carrot "> <input type=reset value="reset"></td></tr></table><p><a href="javascript:history.back();">[back]</a></font>|;
					print qq|</form></div>|;
					&show_dreams;
					print qq|</body></html>|;
				}		
			}
			exit;
		}
	}
	&honoka_sawatari;
	foreach $temp (@main) {
		$adm = not $adm if ($temp =~ /<!--admin_only-->/ && $admin == 0);
		$temp =~ s/<!--admin_only-->//g;
		unless ($adm) {
			if ($temp =~ /<!--data_include-->/) {
				print $dmi;
				chop(@LOG); undef(@RESLOG);
				if ($F{'m'} eq 'ers' ) { $met = "manami"; } elsif ($F{'m'} eq 'edt') { $met = "mariko"; } elsif ($F{'m'} eq 'aru') { &move_yourbody; $met = 'miho'; $xt = qq|enctype="multipart/form-data"|} else { $met = ""; }
				if ($met ne '') {
					print qq|<form method=post action="irisnx.cgi" $xt><input type=hidden name="m" value="$met"><table border=1 cellspacing=0 cellpadding=1>|;
					print qq|<tr><td align=center colspan=6 bgcolor="#ffffff"><font size=2>$eddt</font></td></tr>|;
					print qq|<tr><td align=center colspan=2><font size=1>no</font></td><td><font size=1>name</font></td><td><font size=1>comment</font></td>|;
					print qq|<td><font size=1>bd</font></td><td></td></tr>|;
				}
				foreach $LOG (@LOG) {
					@tempview = @view;
					my(%L); my($img_method);
					%L = &cvt_data($LOG);
					if ($F{'m'} ne 'rfm' || ($F{'m'} eq 'rfm' && $F{'n'} == $L{'num'})) {
						undef(@RESLOG); $sp = 0;
						foreach $RES (@RES) {
							($dtnum, $sgn) = split(/\|/, $RES);
							push(@RESLOG, $RES) if ($L{'num'} == $dtnum);
						}
						@RESLOG = reverse(@RESLOG);
						if ($met eq '') {						
							foreach $tempview (@tempview) {	
								$bdm = not $bdm if ($tempview =~ /<!--admin_only-->/ && $admin == 0);
								$tempview =~ s/<!--admin_only-->//g;
								unless ($bdm) {								
									if ($tempview !~ /<!--reply-->/) {
										$tempview =~ s/(NAME="n")/$1 value="$L{'num'}"/i;
										$tempview =~ s/(NAME="p")/$1 value="$F{'p'}"/i;
										foreach (keys %cookie) { $tempview =~ s/$_<!--d-->/$cookie{$_}/ig; }
										foreach (keys %L ) { $tempview =~ s/$_<!--d-->/$L{$_}/ig; }
										print $tempview; 
									} 
									else { 
										foreach $RESLOG (@RESLOG) {
											my($konnichiwa) = $repl; my(%D);
											%D = &cvt_data($RESLOG);
											foreach $_ ( keys %D ) { $konnichiwa =~ s/$_<!--d-->/$D{$_}/ig; }
											print $konnichiwa;
										}

									}
								}
							}
						} 
						else {						
							&rmv_list($met, %L);
							foreach $RESLOG (@RESLOG) { %D= &cvt_data($RESLOG); &rmv_list($met, %D); }
						}
					}
				}
				if ($met ne '') {
					if ($met eq 'manami') { $strt = qq|<input type=checkbox name=mv value="on">binary data backup |; }
					if ($met eq 'miho') {
						print qq|<tr><td colspan=5 nowrap align=right><font size=2 style="font-size:11px;">upload only</font></td><td align=center><input type=radio name="mizuho" value="" checked></td></tr>|;
						print qq|<tr><td colspan=6 align=center><font size=2>|;
						print qq|replace/upload<input type=file name="file" size=15> <input name=lx type=submit value="do it"></font></td></tr>|;
						print qq|</table></form>|;
						&show_dreams;
					} 
					else {
						print qq|<tr><td colspan=6 align=center>$strt <input type=submit value="do it!"> <input type=reset value="reset"></td></tr>|;
						print qq|</table></form>|;
					}
				}
			} 
			else { 
				foreach (keys %cookie) { $temp =~ s/$_<!--d-->/$cookie{$_}/ig; }
				foreach (keys %V) { $temp =~ s/$_<!--d-->/$V{$_}/ig; }
				$temp =~ s/(NAME="cookie")/$1 $cook/i;
				$temp =~ s/(NAME="n")/$1 value="$F{'n'}"/i if ($F{'m'} eq 'rfm');
				$temp =~ s/(NAME="p")/$1 value="$F{'p'}"/i if ($F{'m'} eq 'rfm');
				$temp =~ s/(NAME="title")/$1 value="$E{'title'}"/ig;
				$temp =~ s/(<\/textarea>)/$E{'comment'}$1/ig;
				print $temp;
			}
		}
	}


exit;

sub show_dreams {
	my($fs); $fs = 1;
	print qq|<div align=center><font size=2>extra box</font><table width=560 cellspacing=0 cellpadding=1 border=1>\n|;
	foreach (keys %FLIST) {
		if ($FLIST{$_} != 11 or $F{'m'} ne 'aru') {
			print "<tr>" if ($fs == 1);
			if ($FLIST{$_} == 1) { $k = '!'; } elsif ($FLIST{$_} == 11) { $k = '~'; } else { $k = 'x'; }
			$ment = ($F{'m'} eq 'aru') ? qq|k<a href="irisnx.cgi?m=k&f=$_">i</a>ll| : ""; 
			$CP = qq|$data_url$_|; 
			print qq|<td width="25%"><font size=2>&nbsp;<a href="$CP" target="_blank">$_</a> (<font color=red>$k</font>)<div align=right><b>$ment</b></div></font></td>\n|;
			$fs++;
			print "</tr>" if ($fs == 5);
		}
	}
	print "</tr>" if ($fs!= 5);
	print qq|</table></div><br><br>|;
}
sub move_yourbody {
	undef(%FLIST);
	opendir(DIR, $data_dir) || &msg_error("Directory Browse", "Can't open $data_dir");
	while (defined($file = readdir(DIR))) { $FLIST{$file}++ if ($file ne '.' && $file ne '..' && $file ne 'irisnx.log' && $file ne 'index.htm'); }
	closedir(DIR);
	foreach  (@TOTLOG) {
		@TMP = split(/\|/, $_);
		$FLIST{$TMP[7]}+= 10 if $TMP[7] !~ /^(http|ftp|telnet):\/\// && $TMP[7] ne '';
	}
}

sub honoka_sawatari
{
	my(@FILE); my($MODE);
	@FILE = &get_file($nx_desc); chomp(@FILE);
	foreach $FILE (@FILE) {
		if ($FILE !~ /^#/) {
			if ($FILE =~ /^%/) {
				$FILE =~ s/^%//;
				if ($FILE eq 'extension') { $MODE = 1; } 
				elsif ($FILE =~ /:/) {
					($enum, $desc) = split(/:/, $FILE, 2);
					$styles[$enum] = $desc; $MODE = 0; 
					$enum=$enum+0;
				} 
				else { $multi = $FILE; $MODE = 2; }
			} 
			else {
				if ($MODE == 1) {
					($desc, $ext) = split(/:/, $FILE);
					@exts = split(/,/, lc($ext));
					foreach (@exts) { $eika{$_} = $desc; }
				} 
				elsif ($MODE == 2) { $neko{"$enum$multi"} .= $FILE; }
			}
		}
	}
	$style_list = '';
	foreach (0 .. $#styles) { $p = ($E{'style'} == $_) ? " selected" : ""; $V{'style_list'} .= qq|<option value="$_"$p>$styles[$_]\n|; }
}

sub moon_crystal { chomp(@TMP); foreach (0 .. $angels) { $F{$sister_princess[$_]} = $TMP[$_]; } }
sub makeup { $MSG = ''; foreach (0 .. $angels) { $MSG .= "$F{$sister_princess[$_]}\|"; } $MSG .= "\n"; &tmp_save("$MSG"); }

sub spt_date {
	my($DATE, $TIME, $wp) = @_; my(%C);
	($C{'yyyy'}, $C{'mm'}, $C{'dd'}) = split(/\//,$DATE);
	($C{'ho'}, $C{'mi'}, $C{'se'}) = split(/:/,$TIME);
	$wp = substr($wp, 0, 1);
	foreach (keys %C) {
		if ($_ eq 'yyyy') { $C{$_} = "0$C{$_}" while (length $C{$_} < 4); }
		else { $C{$_} = "0$C{$_}" while (length $C{$_} < 2); } 
	}
	"$C{'yyyy'}$C{'mm'}$C{'dd'}$C{'ho'}$C{'mi'}$C{'se'}$wp";
}

sub rmv_list {
	my($mest, %A) = @_;
	my($color); my($ldt); my($flag);
	$ldt = substr($A{'comment'}, 0, 60); $ldt =~ s/<BR>//g; $ldt =~ s/</&lt;/g; $ldt =~ s/>/&gt;/g;
	$ldt .= " &nbsp; <i>......</i>" if (length $A{'comment'} > 60);
	if ($mest eq 'manami') { $mtk = "checkbox"; } else { $mtk = "radio"; }
	chomp($A{'filename'});
	if ($A{'filename'} =~ /^(http|ftp|telnet):\/\//) { $CP = $A{'filename'}; } else { $CP = qq|$data_url$A{'filename'}|; }
	if ($A{'filename'} ne '') { $flag = qq|<a href="$CP" target="_blank">○</a>"|; } else { $flag = "Ⅹ"; }
	if ($A{'sn'} eq '') { print qq|<tr><td  bgcolor="#ffffff" align=center colspan=2><font size=3 color=black><b>$A{'num'}</b></font></td><td><font size=2>$A{'name'}</font></td><td><font size=2 style="font-size:11px;">$ldt</font></td><td align=center><font size=1>$flag</font></td><td align=center><input type=$mtk name="mizuho" value="$A{'num'}_$A{'sn'}"></td></tr>\n|; } 
	else { print qq|<tr><td nowrap>&nbsp; &nbsp;</td><td>$A{'sn'}</td><td><font size=2>$A{'name'}</font></td><td><font size=2 style="font-size:11px;">$ldt</font></td><td align=center><font size=1>$flag</font></td><td align=center><input type=$mtk name="mizuho" value="$A{'num'}_$A{'sn'}"></td></tr>\n|; }
}

sub cvt_data {
	my($LOG) = $_[0]; my(%L); my(%A); my(%C);
	($L{'num'}, $L{'sn'}, $L{'name'}, $L{'email'}, $L{'url'}, $L{'time'}, $L{'comment'}, $L{'filename'}, $L{'title'}, $L{'style'}) = split(/\|/, $LOG);
	$L{'name'} = qq|<a href="mailto:$L{'email'}">$L{'name'}</a>| if ($L{'email'} ne '');
	$tmp = $L{'url'}; $L{'url'} = $url; $L{'url'} =~ s/<-!->/$tmp/g;
	$L{'reply'} = $reply_link; $L{'reply'} =~ s/<-!->/irisnx.cgi?m=rfm&p=$F{'p'}&n=$L{'num'}"/g;
	$L{'reply'} = '' if ($F{'m'} eq 'rfm');
	%A = &get_time($L{'time'});
	$rtime = &get_vtime(time);
	%C = &get_time($rtime);
	$rtime=($C{'yyyy'}*97761600+$C{'mm'}*267840+$C{'dd'}*8640+$C{'ho'}*360+$C{'mi'}*6+$C{'se'})-($A{'yyyy'}*97761600+$A{'mm'}*267840+$A{'dd'}*8640+$A{'ho'}*360+$A{'mi'}*6+$A{'se'});
	if ($rtime) {
		if ($rtime < 360) { $clr = $gradcolor; }
		elsif ($rtime > 360 * 24 * 7) { $clr = $gradcolor2; }
		else { 
			$rg = $rtime - 359; 
			@cl1 = $gradcolor =~ /(..)(..)(..)/; @cl2 = $gradcolor2 =~ /(..)(..)(..)/;
			foreach (0 .. 2) { 
				$cl1[$_] = hex($cl1[$_]); $cl2[$_] = hex($cl2[$_]); 
				$cl3[$_] = $cl1[$_] + int(($cl2[$_] - $cl1[$_]) / (360 * 24 * 7) * $rg); 
			}
			$clr = sprintf("%02X%02X%02X",$cl3[0], $cl3[1], $cl3[2]);
		}
	} 
	else { $clr = $gradcolor2; }
	$L{'gradcolor'} = "\#$clr";
	if ($L{'filename'} ne '') {
		$img_method = 0;
		my(@mnext) = split(/\./, $L{'filename'});
		$ext = lc($mnext[$#mnext]);
		if (defined $eika{$ext}) { $neko = $L{'style'}+0 . $eika{$ext}; } else { $neko = $L{'style'}+0 . "extra"; }
		$L{'data'} = $neko{$neko};
		$tmp = $L{'filename'}; $amp = qq|$data_url$L{'filename'}|; 
		if ($L{'filename'} =~ /^(http|ftp|telnet):\/\//) { $amp = $tmp; } else { $amp = qq|$data_url$L{'filename'}|; }
		$L{'data'} =~ s/<-!->/$amp/g;
		$L{'data'} =~ s/<-o->/$tmp/g;
	} 
	else { $L{'data'} = ''; }
	foreach (keys %A) { $L{$_} = $A{$_}; }
	$L{'res'} = $TL{$L{'num'}};
	%L;
}


sub get_form {
    if ($ENV{'QUERY_STRING'}) { &PUrlEncode($ENV{'QUERY_STRING'}); }
    else {
        binmode STDIN;
        read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
        &PUrlEncode($buffer) if ($ENV{'CONTENT_TYPE'} eq 'application/x-www-form-urlencoded');
        &PMultiPart($buffer) if ($ENV{'CONTENT_TYPE'} =~ m#^multipart/form-data#);
    }
}

sub PUrlEncode {
	@pairs = split(/&/, $_[0]);
    foreach $pair (@pairs) {
        ($key, $value) = split(/=/, $pair);
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		$F{$key} = $value; $miko{$value} = 'koishiteiruno' if ($key eq 'mizuho');
    }

}

sub cvt_html {
	foreach (keys %F) {
		if ($_ ne 'file' && $_ !~ /\./) {
			$F{$_} =~ s/^\s+//;		
			if ($html_use == 0 || ($html_use == 1 && $admin == 0)) { 
				$F{$_} =~ s/</&lt;/g; $F{$_} =~ s/>/&gt;/g; $F{$_} =~ s/"/&quot;/g; 
				$F{$_} =~ s/&/&amp;/g;
				$F{$_} =~ s/&amp;\#([0-9]+);/&\#$1;/g;
			}
			$F{$_} =~ s/\|/&#124/g;
			$F{$_} =~ s/(\r\n|\r|\n)/<BR>/g;
		}
	}
	foreach (keys %must) {
		&msg_error("cvt_html", "$_ not found.") if ($must{$_} & 1 and $F{'m'} eq 'reg' and $F{$_} eq '');
		&msg_error("cvt_html", "$_ not found.") if ($must{$_} & 2 and $F{'m'} eq 'res' and $F{$_} eq '');
	}
	$F{'email'} = '' if ($F{'email'} !~ /.+\@.+\..+/);
	$F{'url'} = '' if ($F{'url'} !~ /http:\/\/.{3,}/);
	$F{'comment'} =~ s/(http:\/\/[\w\.\/\~\-\+\=\#\%\&\?\(\);]+)/<A HREF="$1" TARGET="_blank">$1<\/A>/ig if ($autolink == 1 && ($html_use == 0 or ($html_use == 1 && $admin == 0)));
}

sub PMultiPart {
    my(@TmpArray);
    my(@tfile, @path);
    ($boundary = $ENV{'CONTENT_TYPE'}) =~ s/^.*boundary=(.*)/\1/;
    @TmpArray = split(/--$boundary/, $_[0]);
    @TmpArray = splice(@TmpArray, 1, $#TmpArray - 1);
    foreach $Tmp (@TmpArray) {
        ($dump, $line, $value) = split(/\r\n/, $Tmp, 3);
        if ($line =~ /filename/) {
            @tfile = split(/\"/, $line);
            @path = split(/\\/, $tfile[3]);
            $FileName = ($path[@path-1]);
        } 
		else { $FileName = ''; }
        next if ($Tmp =~ /filename=\"\"/);

        $line =~ s/^Content-Disposition: form-data; //;
        (@column) = split( /;\s+/, $line);
        ($name = $column[0]) =~ s/^name="([^"]+)"$/\1/g;

        if ($#column > 0) {
            if ($value =~ /^Content-Type:/) { ($trash, $trash, $value) = split(/\r\n/, $value, 3); }
            else { ($dump, $value) = split(/\r\n/, $value, 2); }
        }
        else {
            ($dump, $value) = split(/\r\n/, $value, 2);
            if (grep(/^$name$/, keys(%FORM))) {
                if (@{FORM{$name}} > 0) { push(@{$F{$name}}, $value); }
                else { $array_value = $F{$name}; undef($F{$name}); $F{$name}[0] = $array_value; push(@{$F{$name}}, $value); }
            }
            else { next if $value =~ /^\s*$/; $F{$name} = $value; chop($F{$name}); chop($F{$name}); }
            next;
        }

        if ($FileName) {
            while(1) {
                $trash = substr($value, -1, 1);
                last unless($trash eq "\n" || $trash eq "\r");
                chop($value);
            }
            $trash = "$name.name";
            $F{$trash} = $FileName;
            $trash = "$name.size";
            $F{$trash} = length($value);
        }
        $F{$name} = $value;
    }
}

sub get_vtime {
	my(@tmp); my($vt);
	if (length $_[0] != 15) {	
		@tmp = localtime($_[0]);
		foreach (0 .. 5) { 
			if ($_ == 4) { $tmp[4] += 1; }
			elsif ($_ == 5) {
				$tmp[5] += 1900 if (length $tmp[5] < 4);
				$tmp[5] += 100 if ($tmp[5] <= 1970);
			}
			$tmp[$_] = "0$tmp[$_]" if ($tmp[$_] < 10);
			$vt = $tmp[$_]. $vt; 
		}
		$vt .= $tmp[6];
	} 
	else { $vt = $_[0]; }
	$vt;
}

sub get_time {

	my(%L); my($vt); my($pt);
	if ($_[0] =~ /^(8|9)/) {
		($L{'se'}, $L{'mi'}, $L{'ho'}, $L{'dd'}, $L{'mm'}, $L{'yyyy'}, $L{'week_p'}, $dummy, $dummy) = localtime($_[0]);
		$L{'yyyy'} += 1900 if length $L{'yyyy'} < 4;
		$L{'yyyy'} += 100 if $L{'yyyy'} <= 1970;
		$L{'mm'} += 1; $L{'week'} = (Sun,Mon,Tue,Wed,Thu,Fri,Sat) [$L{'week_p'}];
		$L{'se'} = "0$L{'se'}"  if $L{'se'} < 10;
		$L{'mi'} = "0$L{'mi'}"  if $L{'mi'} < 10;
		$L{'ho'} = "0$L{'ho'}" if $L{'ho'} < 10;
		$L{'dd'} = "0$L{'dd'}" if $L{'dd'} < 10;
		$L{'mm'} = "0$L{'mm'}" if $L{'mm'} < 10;
		$L{'yy'} = substr($L{'yyyy'}, 2, 2);
	}
	else {
		$L{'yyyy'} = substr($_[0], 0, 4);
		$L{'mm'} = substr($_[0], 4, 2);	
		$L{'dd'} = substr($_[0], 6, 2);
		$L{'ho'} = substr($_[0], 8, 2);
		$L{'mi'} = substr($_[0], 10, 2);
		$L{'se'} = substr($_[0], 12, 2);
		$L{'week_p'} = substr($_[0], 14, 1);
		$L{'week'} = (Sun,Mon,Tue,Wed,Thu,Fri,Sat) [substr($_[0], 14, 1)];
	}
	%L;
}


sub put_cookie {	
	foreach $_ (@_) { $_ =~ s/\|/&\#124;/g; push(@temp, $_); }
	my($name, $email, $url) = @_;

	($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = gmtime(time + 60*60*24*90 );
	$thisday = (Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday)[$wday];
	$month = (Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec)[$mon];
	$year += 1900 if length $year < 4;
	$year += 100 if $year <= 1970;
	$date_gmt = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT", $thisday, $mday, $month, $year, $hour, $min, $sec);

	if ($F{'cookie'} eq 'on') {
		$string = qq(cname\|$name,cemail\|$email,curl\|$url);
		$string =~ s/(\W)/sprintf( "%%%x", ord( $1 ) )/eg;
		print "Set-Cookie: $cookie_id=$string; expires=$date_gmt\n";
		foreach $key (keys %F) { $cookie{"c" . $key} = $F{$key} };
	} else { &get_cookie; }	
}

sub get_cookie {
    @COOKIES = split(/; /,$ENV{'HTTP_COOKIE'});
    foreach (@COOKIES) {
        ($ck_name,$ck_value) = split(/=/,$_);
		$ck_value =~ tr/+/ /;
		$ck_value =~ s/%([a-fA-F0-9]{2})/pack("c",hex($1))/eg;
		$COOKIE{$ck_name} = $ck_value;
    }
	$cookie{'cname'} = $cookie{'cemail'} = $cookie{'curl'} = '';
    @pairs = split(/,/,$COOKIE{$cookie_id});
	foreach $pair (@pairs) {
        ($key, $value) = split(/\|/, $pair);
        $cookie{$key} = $value;
    }
	$cookie{'curl'} = 'http://' if ($cookie{'curl'} eq '');
	$cook = 'checked' if ($cookie{'cname'} eq '');

}

sub header {
	# 수정하지 말아주세요. 최소한의 예의는 지켜주셔야지요.
	print qq|Content-Type: text/html\nPragma: no-cache\n\n<!--\n|;
	print qq|    IRiS nX $ver\n|;
	print qq|    Copyright(c)2000-2001. NvyU. All rights reserved.\n|;
	print qq|    EMAIL : nvyu\@hitel.net\n|;
	print qq|    U R L : http://nvyu.net/\n-->\n|;
}

sub get_file {
	open(FILEGET, "$_[0]"); @FILEGET = <FILEGET>; 
	close(FILEGET) or &msg_error("get_file", "could not read $_[0].");
	@FILEGET;
}

sub put_file {
	($filename, @putdata) = @_;
	open(FILEPUT, ">$_[0]"); print FILEPUT @putdata;
	close(FILEPUT) or &msg_error("put_file", "could not read $_[0].");
}

sub sav_file {
	my($filename);
	$filename = &get_filename($data_dir, $F{'file.name'});
	($dummy, $ext) = split(/\./, $F{'file.name'});
	&msg_error("sav_file", "allowed files only!!") if ($must_allowed == 1 && !defined $eika{lc($ext)});
	&msg_error("sav_file", "file is too big!<br>limited bytes : $img_limit kb") if ($img_limit != 0 && length $F{'file'} > $img_limit * 1024);
	open(FILE, ">$data_dir$filename") || &msg_error("sav_file", "file creating error!<br>please check the permission of directories!");
	binmode FILE; print FILE $F{'file'};
	close(FILE) || &msg_error("sav_file", "file save false. it may not enough disk space.");
	close(TMPFILE);
	$filename;
}

sub tmp_save {
	open(TMPFILE, ">$tmpfile") || &msg_error("sav_file", "file creating error!<br>please check the permission of directories!");
	print TMPFILE $_[0]; close(TMPFILE) || &msg_error("sav_file", "file save false. it may not enough disk space!");
	unlink($tmpfile);
}
sub get_filename {
	my($filename);
	if (-e "$_[0]$_[1]") {
		my($fname, $ext) = split(/\./, $_[1]);
		$ext = ".$ext" if ($ext ne '');
		$filename = "$fname$knum$ext";
		while (-e "$data_dir$filename") { $knum += 1; $filename = "$fname$knum$ext"; }
	} 
	else { $filename = $_[1]; }
	$filename;
}


sub get_pagebar {	
	my($page_now, $page_total, $style) = @_;
	local $ppp = 6;
	$b_p = $page_now - $ppp / 2; $b_p = 1 if $b_p < 1;
	$e_p = $b_p + $ppp;
	if ($e_p > $page_total) { $e_p = $page_total; $b_p = $e_p - $ppp; $b_p = 1 if $b_p < 1; }
	$pages .= qq|<a href="irisnx.cgi?m=$F{'m'}&p=1">[1]</a>...| if ($b_p > 1 && $style == 0);
	for ($i = $b_p; $i <= $e_p; $i++) {
		if ($page_now == $i) { $pages .= "<b>[$i]</b>"; }
		else { $pages .= qq|<a href="irisnx.cgi?m=$F{'m'}&p=$i">[$i]</a>|; }
	}
	$pages .= qq|...<a href="irisnx.cgi?m=$F{'m'}&p=$page_total">[$page_total]</a>| if ($e_p < $page_total && $style == 0);
	$pages;

}

sub log_limit {
	my(@pai) = @_;
	$count = 0; $giveit = 0; $prt = '';
	foreach $aoi (@pai) {
		@TMP = split(/\|/, $aoi); $filename = '';
		if ($TMP[0] != $prt) { $count += 1; $prt = $TMP[0]; }
		if ($count > $max || ($giveit != 0 && $TMP[0] == $giveit)) {
			$giveit = $TMP[0];
			if ($TMP[7] ne '' && $TMP[7] !~ /^(http|ftp|telnet):\/\//) {
				$filename = &get_filename($backup_dir, $TMP[7]);
				rename("$data_dir$TMP[7]", "$backup_dir$filename");
			}
			if ($TMP[7] ne $filename) { $TMP[7] = $filename; $aoi = ""; foreach (0 .. $angels) { $aoi = "$TMP[$_]\|"; } $aoi .= "\n"; }
			push(@OLDLOG, $aoi);			
		}
		else { push(@paichan, $aoi); }
	}
	if ($giveit != 0) {
		@BLOG = &get_file($backup_log);
		unshift(@BLOG, @OLDLOG);
		&put_file($backup_log, @BLOG);
	}
	@paichan;
}
sub lock {
	my($retry) = 10; my($flag) = 0;
	if ($lock == 1) { 
		while (!symlink(".", $lockfile)) {
			if (--$retry <=0 ) { unlink($lockfile) if (-e $lockfile); &msg_error("File Lock", "$!"); }
			sleep(1);
		}
	} elsif ($lock == 2) {
		foreach (1 .. $retry) {
			if (-e "$lockfile") { sleep(1); }
			else { open(LOCK, ">$lockfile"); close(LOCK) || &msg_error("File Lock", "$!"); $flag = 1; last; }
		}
		&msg_error("File Lock", "$!") if ($flag == 0);
	}
}

sub unlock { unlink($lockfile) if (-e $lockfile); }

sub msg_error {
	local($location, $message, $flag) = @_;
	print "Content-type: text/html\nPragma: no-cache\n\n";
	if ($flag eq '') {
		print "<HTML><HEAD><TITLE>500 CGI internal Error</TITLE></HEAD>";
		print qq|<table width=100% height=95%><tr><td align=center><table border=1 cellspacing=1 cellpadding=5 bgcolor="#fededd"><tr><td align=center><B>500 CGI Internal Error</b><hr><font size=2>$soft - $ver ($location)<br><b>ERROR : $message</b><br>Please contact to <a href="mailto:$email">admin</a> for report this error.<br></font></td></tr></table><font size=1><br>presented from <a href="http://nvyu.net" target="_blank">-=starry scape=-</a></font></td></tr></table>|;
		&unlock;
		exit;
	} 
	else {
		print "<HTML><HEAD><TITLE>INFO</TITLE></HEAD>";
		print qq|<table width=100% height=95%><tr><td align=center><table border=1 cellspacing=1 cellpadding=5 bgcolor="#defedd"><tr><td align=center><B>INFORMATION</b><hr><font size=2>$soft - $ver ($location)<br><b>$message</b></font></td></tr></table><font size=1><br>return to <a href="./irisnx.cgi?m=$flag">IRiS nX</a></font></td></tr></table>|;
		exit;
	}
}

END { $EndClock = (times)[0]; printf "\n<!--nX RUNNING TIME / %.3f-->", $EndClock - $StartClock; }