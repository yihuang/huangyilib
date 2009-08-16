Douban = new Object();
Douban.errdetail = [
    '','未知错误','文件过大',
    '信息不全','域名错误','分类错误',
    '用户错误','权限不足','没有文件',
    '保存文件错误','不支持的文件格式','超时',
    '文件格式有误','','添加文件出错',
    '已经达到容量上限','不存在的相册','删除失败',
    '错误的MP3文件','有禁用的内容,请修改重试']
var trace = function(o){
    if(!/^http:\/\/www/.test(location.href) && window.console && window.console.info){
        console.info(arguments);
    }
}

var report = function(s){$.get('/j/report?e='+s)}
Douban.EventMonitor = function(){
    this.listeners = new Object();
}

Douban.EventMonitor.prototype.broadcast=function(widgetObj, msg, data){
    var lst = this.listeners[msg];
    if(lst != null){
        for(var o in lst){
            lst[o](widgetObj, data);
        }
    }
}
Douban.EventMonitor.prototype.subscribe=function(msg, callback){
    var lst = this.listeners[msg];
    if (lst) {
        lst.push(callback);
    } else {
        this.listeners[msg] = [callback];
    }
}
Douban.EventMonitor.prototype.unsubscribe=function(msg, callback){
    var lst = this.listener[msg];
    if (lst != null){
        lst = lst.filter(function(ele, index, arr){return ele!=callback;});
    }
}

// Page scope event-monitor obj.
var event_monitor = new Douban.EventMonitor();

function load_event_monitor(root) {
    var re = /a_(\w+)/;
    var fns = {};
    $(".j", root).each(function(i) {
        var m = re.exec(this.className);
        if (m) {
            var f = fns[m[1]];
            if (!f) {
                f = eval("Douban.init_"+m[1]);
                fns[m[1]] = f;
            }
            f && f(this);
        }
    });
}

function request_log_ad_displays() {
    $('div[@id^="daslot"]').each(function(i) {
        var id = $(this).attr('id');
        params = id.split("-");
        $.get("/j/da/view?da="+ params[1] + "&dag=" + params[2]
            + "&dac=" + params[3] + "&p=" + params[4] + "&kws="
            + params[5]);
    });
}

$(function() {
    load_event_monitor(document);
    request_log_ad_displays();
});

Douban.prettify_form = function(form) {
    $('input:submit', form).each(function(i) {
        var btn = $('<a href="#" class="butt"></a>').text($(this).val());
        btn.click(function() {
            if(clean_tip()) form.submit();
            return false;
        });
        $(this).hide().after(btn);
    });
}

var get_form_fields = function(form) {
    var param = {};
    $(':input', form).each(function(i){
        var name = this.name;
        if (this.type == 'radio') {
            if (this.checked) param[name] = this.value;
        } else if (this.type == 'checkbox') {
            if (this.checked) param[name] = this.value;
        } else if (this.type == 'submit'){
            if (/selected/.test(this.className)) param[name] = this.value;
        } else {
            if (name) param[name] = this.value;
        }
        if(/notnull/.test(this.className) && this.value == ''){
            $(this).prev().addClass('errnotnull');
            param['err'] = 'notnull';
        }
    });
    return param;
}

var remote_submit_json = function(form, func, disable, action) {
    var fvalue = get_form_fields(form);
    if(fvalue['err'] != undefined) return;
    $(':submit,:input',form).attr('disabled',disable==false?0:1);
    var act = action || form.action;
    $.post_withck(act, fvalue, function(ret){
        var json = eval('('+ret+')'); func(json);
    });
}

/* entry vote button */
Douban.init_evb = function(o) {
    var eid = $(o).attr("id").split("-")[1];
    $(o).submit(function() {
        var url = "/j/entry/" + eid + "/vote";
        $.post_withck(url, function(ret) {
            var r = eval("("+ret+")");
            event_monitor.broadcast(this, "entry_"+eid+"_voted", r);
            $(o).text("你的投票已经提交，谢谢。")
            $("#nf-"+eid).hide();
            $("#nf_s-"+eid).hide();
        });
        return false;
    });
}

/* entry vote count */
Douban.init_evc = function(o) {
    var eid = $(o).attr("id").split("-")[1];
    event_monitor.subscribe("entry_"+eid+"_voted", function(caller, data) {
        var count = data.rec_count;
        if (count) {
            $(o).text(""+count+"人推荐").removeClass("hidden");
        }
    });
}

/* entry nointerest button */
Douban.init_enb = function(o) {
    var eid = $(o).attr("id").split("-")[1];
    $(o).submit(function() {
        var url = "/j/entry/" + eid + "/nointerest";
        $.post_withck(url, function(ret) {
            $(o).text("你的投票已经提交，谢谢。");
            $("#a_evb-"+eid+",#evb_s-"+eid).hide();
        });
        return false;
    });
}

var voteuse_act = function(useful, id, type, isnew) {
    var url = "/j/" + type + "/" + id + (useful?"/useful":"/useless");
    $.postJSON_withck(url, {}, function(ret){
        if (ret.result) {
            if(isnew){
                var u = $('#ucount'+id+'u'),l = $('#ucount'+id+'l');
                if ((u.text() == ret.usecount) && 
                    (l.text()==ret.totalcount - ret.usecount) &&
                    (ret.result != 'notself')){
                    alert('你已经投过票了');
                }
                u.html(ret.usecount);
                l.html(ret.totalcount-ret.usecount);
            }else{
                $('#voteuse_'+id).html('<span class="m gtleft">你的投票已经提交，谢谢。</span>');
                $('#userate_'+id).html('<p id="userate_%s" class="pl">' + ret.usecount + '/' + ret.totalcount + '的人觉得此评论有用:</p>');
            }
        }
        return false;
    });
}

var voteuseful = function(id, isnew) {
    var _ = id.split('-');
    var type = (_[0]=='d')?"doulist":"review";
    return voteuse_act(true, _[1], type, isnew);
}

var voteuseless = function(id, isnew) {
    var _ = id.split('-');
    var type = (_[0]=='d')?"doulist":"review";
    return voteuse_act(false, _[1], type, isnew);
}

var votegood = function(id) {
    $.postJSON_withck('/j/review/'+id+'/good',function(r){
        var g = $('#ucount'+id+'g');
        if (g.text() == r.count && r.result != 'notself'){
            alert('你已经投过票了');
        }
        g.html(r.count);
    });
}
/* blog entry folding */
Douban.init_bef = function(o) {
    var eid = $(o).attr('id').split('entry-')[1],
    unfolder = $('.unfolder',o),folder = $('.folder',o),
    s = $('.entry-summary',o), f = $('.entry-full',o);
    unfolder.click(function(){
        if(f.text() == ""){
            var loadtip = $('<div class="loadtip">正在载入...</div>');
            var loadhl = setTimeout(function(){$('.source',o).before(loadtip);}, 200);
            var url = '/j/entry/'+eid+'/';
            $.getJSON(url, function(j){
                clearTimeout(loadhl);
                loadtip.hide();
                $.post_withck(url+'view', {});
                f.html(j.content).find('a').attr('target','_blank');
                f.show();
                s.hide();
            });
        }else{
            f.show();
            s.hide();
        }
        unfolder.hide();
        folder.show();
        return false;
    }).hover_fold('unfolder');

    folder.click(function(){
        s.show();
        f.hide();
        folder.hide();
        unfolder.show();
    }).hover_fold('folder');
}

Douban.init_unfolder_n = function(o){
    $(o).click(function(){
        var rid = $(o).attr('id').split('-')[1];
        var url = '/j/note/'+rid+'/full';
        $.getJSON(url, function(r) {
            $('#note_'+rid+'_short').hide();
            $('#note_'+rid+'_full').html(r.html);
            $('#note_'+rid+'_full').show();
            $('#note_'+rid+'_footer').show();
            $('#naf-'+rid).hide();
            $('#nau-'+rid).show();
            load_event_monitor($('#note_'+rid+'_full'));
        });
        return false;
    }).hover_fold('unfolder');
}

Douban.init_folder_n = function(o){
	$(o).click(function(){
		var rid = $(o).attr('id').split('-')[1];
		$('#note_'+rid+'_full').hide();
		$('#note_'+rid+'_short').show();
		$('#note_'+rid+'_footer').hide();
		$(o).hide();
		$('#naf-'+rid).show();
	}).hover_fold('folder');
}

Douban.init_unfolder = function(o){
    $(o).click(function(){
        var rid = o.id.split('-')[1];
        var url = '/j/review/'+rid+'/fullinfo';
        $.getJSON(url, function(r) {
            $('#review_'+rid+'_short').hide();
            $('#review_'+rid+'_full')[0].innerHTML = r.html
            $('#review_'+rid+'_full').show();
            $('#af-'+rid).hide();
            $('#au-'+rid).show();
            load_event_monitor($('#review_'+rid+'_full'));
        });
        return false;
    }).hover_fold('unfolder');
}

Douban.init_folder = function(o){
    $(o).click(function(){
        var rid = $(o).attr('id').split('-')[1];
        $('#review_'+rid+'_full').hide();
        $('#review_'+rid+'_short').show();
        $(o).hide();
        $('#af-'+rid).show();
    }).hover_fold('folder');
}

/* blog entry voters folding */
Douban.init_bevf = function(o) {
    var eid = $(o).attr('id').split('bevs-')[1];
    var h = $('.voters_header',o);
    if (!h.length) return;
    h.hover(function(){$(this).addClass('clickable_title');},
        function(){$(this).removeClass('clickable_title');});
    var v = $('#vsl',o);
    var l = $('.link', o);
    var m = $('#more_voters',o);

    var fn = function(e) {
        var f = $(".mv",o);
        if (f.length) {
            var d = f.toggle().css('display');
            l.text(d=='none' ? "更多推荐者" : "隐藏");
            if (m.length)
                m.toggle().css('display');
        } else {
            t=$('<li>正在装载...</li>');
            if (v.length) {
                v.append(t);
            } else {
                h.after(v=$('<ul id="vsl" class="user-list pl indent"></ul>'));
                v.append(t);
            }
            var url = '/j/entry/'+eid+'/voters?start=8';
            $.getJSON(url, function(j) {
                t.css('display','none');
                t.before($(j.html));
                if (m.length) {
                    m.css('display','none');
                }
            });
            $('.link', o).text("隐藏");
        }
        return false;
    }
    h.click(fn);
    l.click(fn);
};

Douban.init_guidelink = function(o) {
    $(o).click(function() {
        window.open('/help/guide1', '', 'width=640,height=400');
        return false;
    });
};

Douban.init_closelink = function(o) {
    $('<a href="#">关闭</a>').appendTo($(o)).click(function() {
        window.close();
        return false;
    });
};

function ext_links() {
    es = $('.entry-summary');
    es.each(function (i) {
        var a = $(es[i]).find('a');
        a.each(function (j) {
            a[j].target = '_blank';
        });
    });
}

Douban.init_confirm_link = function(o) {
    if(!o.name){
        $(o).click(function(){
            var text = o.title || $(o).text();
            return confirm("真的要"+text+"?");
        });
    } else {
        var _ = o.name.split('-');
        var link = $(o).attr('href').split('/');
        var pid = link[0] != 'http:' ? link[2] : link[4];
        var url = '/j/rec_comment';
        $(o).click(function(){
            var bln = confirm("真的要删除?");
            if(bln){
                $.getJSON(url,{rid: _[1], del_comment: _[2]}, function(){
                    $(o).parent().parent().parent().remove();
                })
            }
            return false;
        })
    }
}

var populate_tag_btns = function(title, div, tags, hash){
    if (tags.length) {
        var p = $('<dl><dt>'+title+'</dt></dl>'),d = $('<dd></dd>');
        $.each(tags, function(i,tag) {
            var btn = $('<span class="tagbtn"/>').addClass(hash[tag.toLowerCase()]?'rdact':'gract').text(tag);
            d.append(btn).append(' &nbsp; ');
        });
    p.append(d);
        div.append(p);
    }
}

Douban.init_interest_form = function(form) {
    var btns = {}, selected = {};
    var select = function(tl) {
        if (btns[tl]) {
            selected[tl] = true;
            $.each(btns[tl], function(i, btn) {
                $(btn).removeClass('gract').addClass('rdact');
            });
        }
    }
    var deselect = function(tl) {
        if (btns[tl]) {
            delete selected[tl];
            $.each(btns[tl], function(i, btn) {
                $(btn).removeClass('rdact').addClass('gract');
            });
        }
    }
    var update = function() {
        var tags = $.trim(form.tags.value.toLowerCase()).split(' '), hash = {};
        $.each(tags, function(i, t){
            if (t != '') { select(t); hash[t] = true; }
        });
        for (t in selected) { if (!hash[t]) deselect(t) }
    };

    update();
    if($(form).data('comment')){
        form.comment.focus();
    }
    else if($('#foldcollect').val() == 'U'){
        form.tags.focus();
    }

    $(form).submit(function() {
        var sid = $(this).attr('action').split('/')[3];
        remote_submit_json(this, function(data){
            if (data.r != 0){
                $('#saving').remove();
                $('#submits').show();
                $('#error').html(Douban.errdetail[data.r]);
                refine_dialog();
                return
            }
            $("#collect_form_"+sid).html('')
            if ($(form).data('reload')) {
                if (/subject\/\d+\/comments/.test(location.href)){
                    location.href = location.href.split('?sort')[0] + '?sort=time';
                }else{
                    location.href = location.href.split('?')[0];
                }
            }else{
                close_dialog();
            }
        },false);
        $('#submits').hide().after('<span class="m" id="saving">正在保存...</span>');
        refine_dialog();
        return false;
    });
    $(form.cancel).click(function(){
        var sid = $(form).attr('action').split('/')[3];
        $("#collect_form_"+sid).html('');
    });

    $('.tagbtn', form).each(function(i){
        var tl = $(this).text().toLowerCase();
        if (btns[tl]) btns[tl].push(this);
        else btns[tl] = [this];
    }).click(function(){
        var tag = $(this).text();
        var tags = $.trim(form.tags.value).split(' '), present=false, tl=tag.toLowerCase(), i;
        tags = $.grep(tags, function(t, i){
                if (t.toLowerCase() == tl) {
                        deselect(tl); present=true; return false;
                } else return true;
        });
        if (!present) { tags.push(tag); select(tl); }
        var content = tags.join(' ');
        form.tags.value = (content.length > 1) ? content+' ' : content;
        form.tags.focus();
    });

    $(form.tags).keyup(update);
}

Douban.init_stars = function(o){
    var ratewords = {1:'很差', 2:'较差', 3:'还行', 4:'推荐', 5:'力荐'}, 
    n = $('#n_rating'), s = $('#stars img'),
    f = function(i) {
        var rating = n.val() || 0;
        s.each(function(j){
            var gif =  this.src.replace(/\w*\.gif$/, ((j<i) ? 'sth' : ((j<rating) ? 'st' : 'nst')) + '.gif');
            this.src = gif;
        });
        if (i) {
                $('#rateword').text(ratewords[i]);
        } else {
                $('#rateword').text(rating ? ratewords[rating] : '');
        }
    }

    s.mouseover(function(){
        f(this.id.charAt(4));
    }).mouseout(f);

    if(n.attr('name')){
        s.click(function(){
            var rating = this.id.charAt(4);
            n.val(rating);
            f(rating);
        });
    }
    f();
}

Douban.init_show_add_friend = function(o) {
    var uid = $(o).attr('id').split('showaf_')[1];
    $(o).click(function() {
        url="/j/people/"+uid+"/friendform";
        $.get(url, {}, function(ret) {
            friend_form_update(ret, uid);
        });
        return false;
    });
}

Douban.init_tries_to_listen = function(o) {
    var m = $(o).attr('name');
    $(o).click(function(){
        var isFF=!document.all;
        if(m!=''){
            var _ = m.split('-')
            var w = _[0];
            var h = _[1];
        }
        else{
            var w = 384;
            var h = 450;
        }
        var left = (screen.width-w)/2;
        var top = isFF?(screen.height-h)/2:50;
        window.open($(o).attr('href'),'','width='+w+',height='+h+',top='+top+',left='+left+',scrollbars=0,resizable=0,status=1');
        return false;
    });
}

Douban.init_discover = function(o){
    var txt = $('#discover_text')[0]
    $(o).submit(function(form) {
        if(!txt.value || txt.value == txt.title) return false
    	var cat = "";
    	cat = $(":radio:checked")[0].value;
    	if (cat == "event"){
    		$("#discover_s").attr("action","/event/search");
    	}else if (cat == "group"){
            $("#discover_s").attr("action","/group/search?q="+$("#discover_text").value);
        }else{
            $("#discover_s").attr("action","/subject_search");
        }
    });
    $(o,':radio').click(function(){
        txt.focus();
    })
}

var friend_form_update = function(data, uid) {
    $("#divac").html(data);
    $("#submitac").submit(function(){
        this.action = "/j/people/"+uid+"/friend";
        remote_submit_json(this,function(r) {
            $("#divac").parent().html(r['html']);
            $("#tip_wait").yellow_fade();
            load_event_monitor($(data));
        });
        return false;
    });
    $("#cancelac").click(function(){
        $("#divac").html("");
    });
}

Douban.init_review_full = function(o) {
    var i = $(o).attr('id').split('_');
    var rid = i[1];
    var stype = i[2];
    $('.link', o).click(function(){
        var url = '/j/review/'+rid+'/'+stype;
        $.getJSON(url, function(r) {
            $(o).html(r.html);
            load_event_monitor($(o));
        });
        return false;
   });
}

Douban.init_show_login = function(o){
    $(o).click(function(){
        return pop_win.load('/js/pop_win/login')
    });
}

Douban.init_show_signup_table = function(o){
    $(o).click(function(){
		event_id = window.location.href.split('/')[4];
        return pop_win.load('/j/event/'+event_id+'/signup')
    });
}

var set_cookie = function(dict, days){
    days = days || 30;
    var date = new Date();
    date.setTime(date.getTime()+(days*24*60*60*1000));
    var expires = "; expires="+date.toGMTString();
    for (var i in dict){
        document.cookie = i+"="+dict[i]+expires+"; path=/";
    }
}

function get_cookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) {
            return c.substring(nameEQ.length,c.length).replace(/\"/g,'');
        }
    }
    return null;
}

Douban.init_hideme = function(o){
    $(o).click(function(){
        $(this).parent().parent().parent().hide();
    });
}

Douban.init_more = function(o){
    $(o).click(function(){
        lastObj = $(this).prev().find("input");
        ids = /(.*_)(\d+)$/.exec( lastObj.attr("id"));
        id = ids[1] + (parseInt(ids[2]) + 1);
        a = lastObj.clone();
        a.attr("value","");
        $(this).before('<br/>').before(a);
        a.attr('id',id).attr('name',id).wrap('<span></span>');
    })
}

Douban.init_search_text = function(o){
    if(!o.value || o.value == o.title){
        $(o).addClass("greyinput");
        o.value = o.title;
    }
    $(o).focus(function(){
        $(o).removeClass("greyinput");
        if(o.value == o.title) o.value = "";
    });
    $(o).blur(function(){
        if(!o.value){
            $(o).addClass("greyinput");
            o.value = o.title;
        }
    });
}

Douban.init_checkreg = function(o){
    $(o).find('.butt').click(function(){
        var check = true;
        $(o).find('input').each(function(){
            if(this.type!='submit' && this.type!='button'){
                if(this.value == ''){
                    $(this).next().css('display','inline');
                    check = false;
                }else{
                    $(this).next().css('display','none');
                }
            }
        });
        return check;
    });
}

Douban.init_click_tip = function(o){
    var tip = $(o).next('.blocktip');
    $(o).click(function(){
        tip.show().blur_hide();
        m = tip.width() + tip.pos().x - $.viewport_size()[0] > 0?
            -tip.width() : 0;
        tip.css('margin-left', m);
    })
    $('.hideme',tip).click(function(){ tip.hide(); })
}

function clean_tip(){
    var txt = $('#page_focus')[0];
    return txt && txt.value != txt.title
}

Douban.init_submit_link = function(o){
	$(o).click(function(){
		$(o).parent().submit();
	});
}

var nowmenu = null;
var hidemenu = function(a){
	a.find('.down').css('display','inline');
	a.find('.up').hide();
	a.next().hide();
	nowmenu = null;
	$('body').unbind('mousedown');
}

var openmenu = function(a){
	if(nowmenu != null){
		hidemenu(nowmenu);
	}
	a.find('.up').css('display','inline');
	a.find('.down').hide();
	a.next().show();
	nowmenu = a;
	$('body').mousedown(function(){
		if(a.parent().attr('rel') != 'on'){
			hidemenu(a);
		}
	});
}

$(function(){
    $("a","#dsearch").each(function(){
        $(this).click(function(){
            if(!clean_tip()) return true;
            urls = $(this).attr("href").split("?cat=");
            $("#ssform").attr("action", urls[0]);
            if(urls[1] != undefined){
                $('<input type="hidden" name="cat" value="' + urls[1] + '" />').appendTo($("#ssform"));
            }
            $("#ssform").submit();
            return false; 
        });
    });
    $('.arrow').click(function(){
        if($(this).find('.up').is(':hidden')){
            openmenu($(this));
        }else{
            hidemenu($(this));
        }
        this.blur();
    });

    $('.arrow').parent().hover(function(){
        $(this).attr('rel','on');
    },function(){
        $(this).attr('rel','off');
    })
    if($.suggest) $('#page_focus').suggest('/j/subject_suggest',{onSelect : function(){
        $(this).parents('form')
        .append('<span><input name="add" value="1" type="hidden"/></span>')
        .submit();
    }})

    $(document.links).click(function(){
        for(var i=0,t=$(this);i<10 && t[0]!=document;t=t.parent(),i++){
            if(t[0].id){
                set_cookie({f:t[0].id});
                break
            }
        }
    })
    var rcoo = get_cookie('report');
    if (rcoo){
        set_cookie({report:''},0);
        $.get('/stat.html?'+rcoo)
    }
    $(':submit').each(function(){
        if ($(this).val() == '加上去'){
            $(this).click(function(){var self = this; setTimeout(function(){self.disabled = 1;},0)})
        }
    })
})

var show_dialog = function(div) {
    if($('#dialog').length) return;
    $('body').prepend('<div id="overlay"></div><div id="dialog"></div>');
    if(div != null){
        $('#dialog').html(div);
    }else{
        $('#dialog').html("<div class='loadpop'>正在载入，请稍候...</div>");
    }
    set_overlay();
}

var set_overlay = function(){
    var oheight = ($.browser.msie?11:26),
        dialog=$('#dialog')[0],
        w=dialog.offsetWidth,
        left=(document.body.offsetWidth-w)/2+'px';

    $('#overlay').css({height:dialog.offsetHeight+oheight,width:w+26,left:left});
    dialog.style.left=left;
}

var close_dialog = function() {
    $('#overlay').unbind('click');
    $('#dialog,#overlay,.bgi').remove();
    if (typeof document.body.style.maxHeight == "undefined") {//if IE6
        $('body','html').css({height: 'auto', width: 'auto'});
        $('html').css('overflow', '');
    }
    document.onkeydown = '';
    return false;
}

var refine_dialog = function(){
    if (!$('#dialog').length) return;
    var agent = navigator.userAgent.toLowerCase();
    var top = 0.5 * ($.viewport_size()[1] - $('#dialog')[0].offsetHeight) + 140;
    $('#dialog,#overlay').css('top', top);
    set_overlay();
}

Douban.init_show_full = function(o){
    $(o).click(function(){
        $(o).parents('.short').hide();
        $(o).parents('.short').next().show();
    })
}

Douban.init_show_short = function(o){
    $(o).click(function(){
        $(o).parents('.all').hide();
        $(o).parents('.all').prev().show();
    })
}

Douban.init_collect_btn = function(o) {
    $(o).click(function(){
        if($('#hiddendialog').length){
            show_dialog($('#hiddendialog').html());
            load_event_monitor($('#dialog'));
        }else{
            show_dialog(null);
            var _ = $(this).attr('name').split('-'),
            btn_type = _[0], sid = _[1],
            interest = _[2], rating = _[3],
            url = '/j/subject/'+sid+'/interest?'+
                (interest ? 'interest='+interest : '')+
                (rating ? '&rating='+rating : '')+
                (btn_type == 'cbtn' ? '&cmt=1':'');
            $.getJSON(url, function(r) {
                if($('#dialog').length){
                    var html = $('<div></div>').html(r.html);
                    var tags = r.tags;
                    var content = tags.join(' ');
                    $('input[@name=tags]', html).val((content.length > 1)? content + ' ' : content)
                    var hash = {};
                    $.each(tags, function(i,tag){hash[tag.toLowerCase()]=true;});
                    populate_tag_btns('我的标签:', $('#mytags', html), r['my_tags'], hash);
                    populate_tag_btns("常用标签:", $('#populartags', html), r['popular_tags'], hash);
                    if (btn_type == 'pbtn' || btn_type == 'cbtn') 
                        $('form', html).data('reload',1);
                    $('#dialog').html(html);
                    $('#showtags').click(function(){
                        if($('#advtags').is(':hidden')){
                            $(this).html('缩起 ▲');
                            $('#advtags').show();
                            $('#foldcollect').val('U');
                        }else{
                            $(this).html($(this).attr('rel'));
                            $('#advtags').hide();
                            $('#foldcollect').val('F');
                        }
                        $(this).blur();
                        refine_dialog();
                    })
                    var oprd=$("input[name=interest]"),rate=$(".rate_stars"),
                    f = function(){
                        if (oprd[0].checked) {rate.hide()} else {rate.show()}
                        refine_dialog();
                    };
                    oprd.click(f);
                    f();
                    if($('#left_n').length){
                        $('#comment').display_limit(140, $('#left_n'));
                    }
                    if(btn_type == 'cbtn'){
                        var h2 = $('h2','#dialog');
                        h2.text(h2.text().replace('修改','写短评'));
                        if (!oprd[0].checked && oprd[1]) oprd[1].checked = true;
                        $('form', '#dialog').data('comment',1);
                    }
                    load_event_monitor(html);
                }
            });
        }
        return false;
    });
}

Douban.init_nine_collect_btn = function(o) {
    $(o).click(function(){
        var _ = $(this).attr('name').split('-');
        var btn_type = _[0], sid = _[1], interest = _[2];
        var url = '/j/subject/'+sid+'/interest';
        $.getJSON(url, interest && {interest: interest}, function(r) {
            var html = $('<div></div>').html(r.html);
            var tags = r.tags;
            var content = tags.join(' ');
            $('input[@name=tags]', html).val((content.length > 1)? content + ' ' : content);
            var hash = {};
            $.each(tags, function(i,tag){hash[tag.toLowerCase()]=true;});
            populate_tag_btns('我的标签(点击添加):', $('#mytags', html), r.my_tags, hash);
            populate_tag_btns("豆瓣成员常用的标签(点击添加):", $('#populartags', html), r.popular_tags, hash);
            if (btn_type == 'pbtn')
                $('form', html).data('reload',1);
            $("#collect_form_"+sid).html("").append('<p class="ul"></p>').append(html);
            load_event_monitor($("#collect_form_"+sid));
        });
        return false;
    });
}

Douban.init_rec_btn= function(o) {
    var _ = $(o).attr('name').split('-'), url = '/j/recommend',
    rdialog = 'rdialog-' + _[1] + '-' + _[2],
    f = function(){
        var uid = ((_[1] == 'I')&&(_[2]==undefined)) ? $('input',$(o).parent())[0].value : _[2],
        rec = (_[3]==undefined) ? '':_[3],
        fcs = function(type){
            if(type == 'I'){
                var s = $('.text','#dialog');
                if(s.length){
                    if(s[0].value.length){s[1].focus();}
                    else{s[0].focus();}
                }
            }else{
                $('#dialog').find(':submit').focus();
            }
            if ($(o).hasClass('novote')){ //it's a new test version of rec btn
                $('form','#dialog').append('<input name="novote" value="1" type="hidden"/>');
            }
        }
        if($('#' + rdialog).length){
            show_dialog($('#' + rdialog).html());
            load_event_monitor('#dialog');
            fcs(_[1]);
        }else{
            $.getJSON(url, {type:_[1], uid:uid, rec:rec}, function(r){
                show_dialog(r.html);
                if(_[1]!='I'){
                    var rechtml = $('<div id="'+rdialog+'"></div>');
                    rechtml.html(r.html).appendTo('body').hide();
                }
                load_event_monitor('#dialog');
                fcs(_[1]);
            });
        }
        return false;
    }
    $(o).click(f);
    if(_[1] == 'I'){
        $(o).parent().parent().submit(f);
    }
}

Douban.init_rec_form = function(form) {
    form.onsubmit = function(){
        $("#ban_word").remove()
        remote_submit_json(this, function(data){
            if(data.ban){
                $(':submit,:input',form).attr('disabled',false);
$(".recsubmit").before('<div class="attn" style="text-align:center" id="ban_word">你的推荐中有被禁止的内容</div >')
                return
            }
            $('#dialog').html('<div class="loadpop m">推荐已提交</div>');
            set_overlay();
            $('#rec_url_text').attr('value','http://');
                setTimeout(function(){
                $('#dialog, #overlay').fadeOut(close_dialog);
                if($('input[name=type]',form).val() == "I"){
                    document.location.reload();
                }
            },400);
        });
        return false;
    }
    $(form).set_len_limit(140);
}

Douban.init_rec_reply = function(o){
    var _ = o.name.split('-');
    var url = '/j/rec_comment';
    if(!o.rev){
        $(o).attr('rev', 'unfold');
    }
    $(o).click(function(){
        if(o.rev != 'unfold'){
            $(o).parent().parent().next().remove();
            $(o).html($(o).attr('rev'));
            o.rev = 'unfold';
        }else if(o.rel!="polling"){
            o.rel="polling"
            $.getJSON(url, {rid: _[2], type: _[3], n:_[4], ni:_[5]}, function(r){
                $('<div class="recreplylst"></div>').insertAfter($(o).parent().parent()).html(r.html);
                load_event_monitor($(o).parent().parent().next());
                $(o).attr('rev', $(o).html()).text('隐藏回应');
                o.rel=""
            })
        }
        return false;
    })
}

Douban.init_reply_form = function(form){
    $(form).attr('action', $(form).attr('rev'));
    var n = $(form).attr('name');
    $(form).submit(function(){
        remote_submit_json(this, function(r){
            var replst = $(form).parent();
            $(replst).html(r.html);
            load_event_monitor(replst);
	    if (n=='n'){
	    var a = $('<span><a href="javascript:void(0)">添加回应</a></span>');
	    }
	    else
	    {
            var a = $('<span style="margin-left:53px"><a href="javascript:void(0)">添加回应</a></span>');
	    }
            $('form', replst).hide().after(a);
            a.click(function(){
                $(this).prev().show();
                $(this).remove();
            })
        });
        $(':submit',form).attr('disabled', 1);
        return false;
    })
    $(form).set_len_limit(140);
}

Douban.init_video_comment = function(form){
    $(form).submit(function(){
        remote_submit_json(this, function(r){
            var insert_point = $('#comments');
            $(insert_point).html(r.html);
            load_event_monitor(insert_point);
            $(':submit', form).attr('disabled', 0);
            $('textarea', form).attr('disabled', 0);
            $('textarea', form).attr('value', '');
        }, true, '/j/video/add_comment');
        return false;
    })
}

Douban.init_video_del_comment = function(o){
    var _ = $(o).attr('name').split('-');
    $(o).click(function(){
        var text = o.title;
        if(confirm("真的要"+text+"?") == true){
                $.postJSON_withck("/j/video/del_comment", {comment_id: _[1], video_id: _[2]}, function(r){
                    var insert_point = $('#c-'+_[1]);
                    $(insert_point).html("");
                });
            }
        return false;
    })
}

Douban.init_noti_form = function(form){
    $(":submit",form).click(function(){
        $(this).addClass('selected');
    });
    $(form).attr('action','/j/request/');
    $(form).submit(function(){
        form.confirm.disabled = true;
        form.ignore.disabled = true;
        remote_submit_json(this, function(r){
            $(form).parent().html(r.html);
        });
        return false;
    });
}

Douban.init_editable = function(o){
    var disp = $('#display',o), form = $('form',o)[0], a = $('a','#edi');
    var show = function(t){
        if(t != undefined){
            disp.text(t);
            if (disp.text() == ''){
                a.text('点击添加描述').addClass('album_photo');
            }else{
                a.text('修改').removeClass('album_photo');
            }
        }
        disp.show();
        $(form).hide();
        $('#edi').show();
    }
    show(disp.text());
    if(form.name) $(form).set_len_limit(form.name);
    $(form).submit(function(){
        remote_submit_json(form, function(r){
            show(r.desc);
        })
        $('textarea',form)[0].value="正在保存...";
        return false;
    })
    $('.cancel',form).click(function(){show()});
    $('#edi',o).click(function(){
        $('#display,#edi').hide();
        $('input,textarea','form').attr('disabled',0);
        $('textarea',o)[0].value = disp.text();
        $(form).show();
        $('textarea',o).focus();
        return false;
    })
}

Douban.init_show_video = function(o){
    var eid = paras($(o).attr('href'))['from'];
    $(o).css('position','relative').attr('href','javascript:void(0)').attr('target','');
    var overlay = $('<div></div>').addClass('video_overlay');
    $('div',o).append(overlay);
    var fhtml = $('img',o).attr('name');
    $(o).click(function(){
        var closebtn = $('<a href="javascript:void(0)">缩进</a>');
        if(eid != undefined) $.get("/j/recommend?from=" + eid);
        closebtn.click(function(){
            $(o).show();
            $(this).prev().remove();
            $(this).remove();
        })

        $(o).after(closebtn).after($('<em>'+fhtml+'</em>'));
        $(o).hide();
    })
}

Douban.init_morerec = function(o){
    $(o).click(function(){
        var n = $(o).parent().next();
        if(n.is(':hidden')){ n.show()} else {n.next().show()}
        $(o).remove();
    })
}

Douban.init_search_result = function(o){
    $('#sinput').suggest('/j/subject_suggest',{resultsClass : 'rc_results', onSelect:function(){
        $(o).parent().submit();
    }});
    $(o).parent().submit(function(){
        var txt = $('#sinput')[0];
        return txt && txt.value != txt.title
    })
    Douban.init_search_text(o);
}

Douban.init_prompt_link = function(o){
    $(o).click(function(){
        var val = prompt(o.title || '请输入');
        if(val){
            location.href = o.href
            + (o.href.indexOf('?') == -1? '?':'&')
            + o.name + '=' + encodeURIComponent(val);
        }
        return false;
    })
}

$.viewport_size = function(){
	var size = [0, 0];
	if (typeof window.innerWidth != 'undefined'){
		size = [window.innerWidth, window.innerHeight];
	}else if (typeof document.documentElement != 'undefined' && typeof document.documentElement.clientWidth != 'undefined' && document.documentElement.clientWidth != 0){
		size = [document.documentElement.clientWidth, document.documentElement.clientHeight];
	}else{
		size = [document.body.clientWidth, document.body.clientHeight];
	}
	return size;
}

$.ajax_withck = function(options){
    if(options.type=="POST")
        options.data=$.extend(options.data||{},{ck:get_cookie('ck')});
    return $.ajax(options)
}

$.postJSON_withck = function(url, data, callback){
    $.post_withck(url, data, callback, "json");
}

$.post_withck = function( url, data, callback, type ) {
    if ($.isFunction(data)) {
        callback = data;
        data = {};
    }
    return $.ajax({
        type: "POST",
        url: url,
        data: $.extend(data,{ck:get_cookie('ck')}),
        success: callback,
        dataType: type
    });
}

jQuery.fn.extend({
    pos:function() {
        var o = this[0];
        if(o.offsetParent) {
            for(var posX=0, posY=0; o.offsetParent; o=o.offsetParent){
                posX += o.offsetLeft;
                posY += o.offsetTop;
            }
            return {x:posX, y:posY};
        } else return {x:o.x, y:o.y};
    },

    set_len_limit : function(limit){
        var s = this.find(':submit:first');
        var oldv = s.attr('value');
        var check = function(){
            if(this.value && this.value.length > limit){
                s.attr('disabled',1).attr('value','字数不能超过'+limit+'字');
            } else {
                s.attr('disabled',0).attr('value', oldv);
            }
        }
        $('textarea', this).focus(check).blur(check).keydown(check).keyup(check);
    },

    display_limit : function(limit, n){
        var self = this, oldv,
        f = function(e){
            var v = self.val();
            if (v == oldv) return;
            if (v.length>=limit){
                self.val(v.substring(0, limit));
            }
            n.text(limit - self.val().length);
            oldv = self.val();
        };
        this.keyup(f);
        f();
    },

    set_caret: function(){
        if(!$.browser.msie) return;
        var initSetCaret = function(){this.p = document.selection.createRange().duplicate()};
        this.click(initSetCaret).select(initSetCaret).keyup(initSetCaret);
    },

    insert_caret:function(t){
        var o = this[0];
        if(document.all && o.createTextRange && o.p){
            var p=o.p;
            p.text = p.text.charAt(p.text.length-1) == '' ? t+'' : t;
        } else if(o.setSelectionRange){
            var s=o.selectionStart;
            var e=o.selectionEnd;
            var t1=o.value.substring(0,s);
            var t2=o.value.substring(e);
            o.value=t1+t+t2;
            o.focus();
            var len=t.length;
            o.setSelectionRange(s+len,s+len);
            o.blur();
        } else {
            o.value+=t;
        }
    },

    get_sel:function(){
        var o = this[0];
        return document.all && o.createTextRange && o.p ?
            o.p.text : o.setSelectionRange ?
            o.value.substring(o.selectionStart,o.selectionEnd) : '';
    },
    blur_hide:function(){
        var s=this,h=function(){return false};
        s.mousedown(h)
        $().mousedown(function(){
            s.hide().unbind('mousedown',h)
            $().unbind('mousedown',arguments.callee);
        })
        return this;
    },
    yellow_fade:function() {
        var m = 0,setp=1,self=this;
        function _yellow_fade(){
            self.css({backgroundColor:"rgb(100%,100%,"+m+"%)"})
            m += setp;setp+=.5;
            if(m <= 100){
                setTimeout(_yellow_fade,35)
            }else{
                self.css({backgroundColor:""})
            }
        };
        _yellow_fade();
        return this;
    },
    hover_fold:function(type){
        var i = {folder:[1,3], unfolder:[0,2]}, s = function(o,n){
            return function(){$('img',o).attr("src","/pics/arrow"+n+".gif");}
        }
        return this.hover(s(this,i[type][0]),s(this,i[type][1]));
    },
    multiselect:function(opt){
        var nfunc = function(){return true},
        onselect = opt.onselect || nfunc,
        onremove = opt.onremove || nfunc,
        onchange = opt.onchange || nfunc,
        sel = opt.selclass || 'sel',
        values = opt.values || [];
        return this.click(function(){
            var id = /id(\d*)/.exec(this.className)[1],
            i = $.inArray(id, values);
            if(i != -1){
                if (!onremove(this)) return;
                values.splice(i,1);
                $(this).removeClass(sel);
            }else{
                if (!onselect(this)) return;
                values.push(id);
                $(this).addClass(sel);
            }
            onchange(values);
            return false;
        })
    }
})

var check_form = function(form){
    var _re = true;
    $(':input',form).each(function(){
        if((/notnull/.test(this.className) && this.value == '')
            || (/most/.test(this.className) && this.value && this.value.length>/most(\d*)/.exec(this.className)[1]))
        {
            $(this).next().show();
            _re = false;
        }else{
            if(/attn/.test($(this).next().attr('className'))) $(this).next().hide();
        }
    })
    return _re;
}

var paras = function(s){
    var o = {};
    if(s.indexOf('?') == -1) return {};
    var vs = s.split('?')[1].split('&');
    for(var i=0;i<vs.length;i++){
        if(vs[i].indexOf('=') != -1){
            var k = vs[i].split('=');
            eval('o.'+k[0]+'="'+k[1]+'"');
        }
    }
    return o;
}

function delete_reply_notify(id){
    if(!delete_reply_notify.id){
        delete_reply_notify.id=id
        show_dialog($("#confirm_delete").html())
        $('#overlay').css('z-index',100); //workaround for ff2 bug
    }
    return false;
};

function close_delete(is_delete){
    if(is_delete){
        var id=delete_reply_notify.id;
        $.get("/j/remove_notify?id="+id)
        $("#reply_notify_"+id).fadeOut();
    }
    delete_reply_notify.id=null;
    close_dialog()
}

function moreurl(self, dict){
    var more = ['ref='+encodeURIComponent(location.pathname)];
    for (var i in dict) more.push(i + '=' + dict[i]);
    set_cookie({report:more.join('&')})
}

function tip_win(e){
    $(e).next(".blocktip").show().blur_hide();
}

tip_win.hide=function(e){
    $(e).parents(".blocktip").hide()
}

function js_parser(htm){
    var tag="script>",begin="<"+tag,end="</"+tag,pos=pos_pre=0,result=script="";
    while(
        (pos=htm.indexOf(begin,pos))+1
    ){
        result+=htm.substring(pos_pre,pos);
        pos+=8;
        pos_pre=htm.indexOf(end,pos);
        if(pos_pre<0){
            break;
        }
        script+=htm.substring(pos,pos_pre)+";";
        pos_pre+=9;
    }
    result+=htm.substring(pos_pre,htm.length);

    return {
        htm:result,
        js:function(){eval(script)}
    };
}


function center(elem){
    return {
        left:(document.documentElement.offsetWidth-elem.offsetWidth)/2+'px',
        top:(document.documentElement.clientHeight-elem.offsetHeight)*.45+'px'
    }
}

function pop_win(htm,hide_close){
    if(!window.__pop_win){
        var pop_win_bg=document.createElement("div");
        pop_win_bg.className="pop_win_bg"
        document.body.appendChild(pop_win_bg)
        var pop_win_body=document.createElement("div");
        pop_win_body.className="pop_win";
        document.body.appendChild(pop_win_body)
        __pop_win={
            bg:pop_win_bg,body:pop_win_body,
            body_j:$(pop_win_body),bg_j:$(pop_win_bg)
        };
    }
    var b=__pop_win.body,body_j=__pop_win.body_j,dom=js_parser(htm);
    
    if(hide_close!==true)dom.htm='<a onclick="pop_win.close()" href="javascript:;" class="pop_win_close">X</a>'+dom.htm;
    b.innerHTML=dom.htm;
    var cr = center(b);
    if(document.documentElement.clientHeight<b.offsetHeight){
        cr.top = "0";
        cr.height = document.documentElement.clientHeight-40+"px";
        cr.overflow="auto"
    }
    body_j.css({display:"block"}).css(cr).css({visibility:"visible",zIndex:101});
    dom.js();
    pop_win.fit();
    if(!window.XMLHttpRequest){
        __pop_win.bg.style.top=""
    }
}

pop_win.fit=function(){
if(window.__pop_win){
    var b=__pop_win.body;
    __pop_win.bg_j.css({
        height:b.offsetHeight+20+"px",
        width:b.offsetWidth+20+"px",
        left:b.offsetLeft-10+"px",
        top:b.offsetTop-10+"px",
        zIndex:100
    }).show()
    }
}

pop_win.close=function(){
    __pop_win.bg.style.display="none";
    __pop_win.body.innerHTML="";
    __pop_win.body.style.display="none";
}

pop_win.load=function(url,cache){
    pop_win("加载中,请稍等...")
    $.ajax({url:url,success:pop_win,cache:cache||false})
    return false
}

function event_init_tab() {
    $('#tongcheng_tab').click(function() {
        if($('#tongcheng_tab_block').is(':hidden')) {
            show_tongcheng_tab();
            $().click(function() {
                hide_tongcheng_tab();
                $().unbind("click",arguments.callee);
            });
        } else {
            hide_tongcheng_tab();
        }
        return false
    })
}

function show_tongcheng_tab() {
    $('#tongcheng_tab_block').show();
    $('#tongcheng_tab span').addClass('up')
}

function hide_tongcheng_tab() {
    $('#tongcheng_tab_block').hide();
    $('#tongcheng_tab span').removeClass('up')
}

__load_bk=$.fn.load;
$.fn.load_withck = function( url, data, callback ) {
    if ($.isFunction(data)) {
        callback = data;
        data = {};
    }
    return __load_bk.call(this,url,$.extend(data,{ck:get_cookie('ck')}),callback);
}
function exp_dialog(e){
var d=document.documentElement;
return 0 - parseInt(e.offsetHeight / 2) + (TBWindowMargin = d && d.scrollTop || document.body.scrollTop) + 'px'; 
}
function exp_overlay(e){
return 0 - parseInt(e.offsetHeight / 2) + (TBWindowMargin = document.documentElement && document.documentElement.scrollTop || document.body.scrollTop) + 'px'
}
function exp_sort_h2_over(){this.style.backgroundColor="#eeffee"}
function exp_sort_h2_out(){this.style.backgroundColor=""}

function getslider(nbtn,pbtn,mover,url,pp_id){
    var now = 5, max_num = 100, fetch_num = 5, off_set=0, 
    slide = function(n){
        if (now+n>max_num){
            now = max_num;
            nbtn[0].className = 'dis';
        }else if (now+n<5){
            now = 5;
            pbtn[0].className = 'dis';
        }else{
            now += n; 
        }
        pbtn[0].className = now == 5 ?'dis':'';
        nbtn[0].className = now == max_num ?'dis':'';
        off_set = (5-now) * 105;
        mover.animate({ "marginLeft":off_set+"px" }, {duration: 250*Math.abs(n), easing: $.easing.easeOutCirc});
    }
    return function(n){
        if(now + n > fetch_num && fetch_num < max_num){
            $.postJSON_withck(url, {"start":fetch_num,"pp":pp_id}, function(ret){
                if(ret.err){
                    max_num = ret.total;
                    fetch_num += ret.num;
                    n = ret.num;
                    mover.html(mover.html()+ret.more_html);
                    slide(n);
                }
            });
        }else{
            slide(n);
        }
    }
}

Douban.init_song_interest = function(o) {
    var sid = $(o).attr("id").split("-")[1];
    $(o).click(function(){
        var url = "/j/song/" + sid + "/interest"
        var i = $(o).hasClass('interest');
        $.post_withck(url, {'action':(i?'n':'y')},function(ret) {
            $(o).toggleClass('interest');
            if(i)
            { $(o).children().attr({src:"/pics/gray-heart.gif",title:"我喜欢", alt:"我喜欢"});}
            else
            { $(o).children().attr({src: "/pics/red-heart.gif",title:"取消'我喜欢'", alt:"取消'我喜欢'"});}
        });
        return false;
    });
}

Douban.init_vote_comment = function(o){
    var v = $(o).prev().prev(),id = $(o).prev().val();
    $(o).click(function(){
        $.postJSON_withck('/j/comment/vote',{id:id},function(r){
            if(r.count){v.text(r.count)}else{
                alert('这条短评你已经投过票了');
            }
        })
    })
}

Douban.init_rev_text = function(o){
    var form = $(o).parents('form'),
    btn = $('input[name=rev_submit]');
    btn.click(function(){
        if ($(o).val().length<50){
            var sid = /subject\/(\d*)/.exec(location.href)[1];
            $.getJSON('/j/comment/check',{sid:sid},function(r){
                if (r.has){
                    if(confirm('少于50字的评论将被自动转为简短评论。并替换之前发表的简短评论内容。是否继续？')){
                        form.submit(); 
                    }
                }else{
                    form.submit();
                }
            })
            return false;
        }
        return true;
    });
}

Douban.init_popup = function(o){
    $(o).click(function(){
        var size = / (\d+)x(\d+)$/.exec(o.className);
        if(!window.open(o.href,'popup','height='+size[2]+',width='+size[1]+
        ',toolbar=no,menubar=no,scrollbars=no,location=no,status=no')){
            location.href=o.href;
        }
        return false;
    })
}
