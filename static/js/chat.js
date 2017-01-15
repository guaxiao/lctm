var socket = io('http://' + document.domain + ':' + location.port);


var chatStore = {
    '大厅': [],
    '游戏': [],
    '灌水': [],
};

var emojiPanel = function(data) {
  this.e = document.querySelector(data.selector)
  this.func = data.func
  this.emojiList = []
  this.emojiMap = {}
  this.buttonId = `id-${(new Date()).valueOf().toString()}`
  this.init()
}

emojiPanel.prototype.init = function() {
  const t = `
  <div class='div-emoji-main'>
    <div class="div-emoji-button" id="${this.buttonId}">
    </div>
  </div>
  `
  this.e.innerHTML = t;
  const btn = document.querySelector(`#${this.buttonId}`)
  if (this.emojiList.length == 0) {
    api('/emoji').then((emojiList) => {
      this.emojiList = emojiList
      this.emojiList.map((v, i) => {
        this.emojiMap[v.key] = `
          <img class="emoji-img" data-key=${v.key} src=${v.value}>
        `
      })
    })
  }
  btn.onclick = () => {
    const t = `
    <div class="div-emoji-container">
    </div>
    `
    const m = document.querySelector('.div-emoji-main')
    m.innerHTML += t
    const c = document.querySelector('.div-emoji-container')
    var it = ''
    for (let i = 0; i < this.emojiList.length; i++) {
      const emoji = this.emojiList[i]
      const e = `
        <img class="div-emoji-item" data-key=${emoji.key} src=${emoji.value}>
      `
      it += e
    }
    c.innerHTML = it
    this.active()
  }
}

emojiPanel.prototype.active = function() {
  const btn = document.querySelector(`#${this.buttonId}`)
  const container = document.querySelector('.div-emoji-container')
  container.onclick = (e) => {
    if (e.target.localName == 'img') {
      this.func(e.target.dataset.key);
    }
  }

  btn.onclick = () => {
    const e = document.querySelector('.div-emoji-container')
    const t = `
    <div class="div-emoji-container">
    </div>
    `
    e.style.animationName = 'unshow'
    e.addEventListener("webkitAnimationEnd", () => {
      this.init();
    });
  }
}

emojiPanel.prototype.render = function(message) {
  var items = message.split(':')

  var b = items.map((v, i) => {
    return this.emojiMap[`:${v}:`] || `<span>${v}</span>`
  })
  return b.join('')
}

var emoji = new emojiPanel({
  selector: '.emoji',
  func: emojiCallback,
})

emojiPanel.prototype.changeSelector = function(selector) {
  this.e.innerHTML = ''
  this.e = document.querySelector(selector)
}

var ReactionSington = (function() {
  var init;
  var reaction;
  return {
    new: function(data) {
      console.log(init);
      if (init == undefined) {
        init = true;
        reaction = new emojiPanel(data);
        return reaction;
      } else {
        reaction.changeSelector(data.selector);
        reaction.init()
        return reaction
      }
    },
    render: function(data) {
      console.log(reaction);
      return reaction.render(data)
    }
  }
})()

var initChatStore = function() {
  $('.rc-channel').map(function() {
    var channel = $(this).find("a").text();
    chatStore[channel] = [];
  })
}

var currentChannel = '大厅';

var log = function () {
    console.log.apply(console, arguments);
};

// 滚动到底部
var scrollToBottom = function (selector) {
    var height = $(selector).prop("scrollHeight");
    $(selector).animate({
        scrollTop: height
    }, 300);
};

var chatItemTemplate = function (chat) {
    var type = chat.type;
    var name = chat.username;
    var avatar = chat.avatar;
    var time = new Date();

    if (type == 'join') {
        var _t = `
            <div>
                <img src="${avatar}"  height="10" width="10" class="avatar__image" alt="">
                <span>${name} 加入了聊天</span>
            </div>
        `
    } else {
        var content = chat.content;
        var id = chat.id;
        content = emoji.render(content)
        // var time = chat.created_time;
        var staticFileURLPreix = location.origin + '/static/'
        var t = `
        <li class="left clearfix chat-item" data-id=${id}>
          <span class="chat-img pull-left">
            <img src="${staticFileURLPreix + avatar}" alt="User Avatar">
          </span>
          <div class="chat-body clearfix">
            <div class="header">
              <strong class="primary-font">${name}</strong>
              <small class="pull-right text-muted"><i class="fa fa-clock-o"></i> ${time}</small>
            </div>
            <p>
              ${content}
            </p>
            <div class="chat-reaction-list">
            </div>
          </div>

        </li>
        `;
    }

    return t;
};

var insertChats = function (chats) {
    var selector = '#main'
    var chatsDiv = $(selector);
    var html = chats.map(chatItemTemplate);
    chatsDiv.append(html.join(''));
    scrollToBottom(".chat-message");
};

var insertChatItem = function (chat) {
    var selector = '#main'
    var chatsDiv = $(selector);
    var t = chatItemTemplate(chat);
    chatsDiv.append(t);
    scrollToBottom(".chat-message");
}

var chatResponse = function (r) {
    var chat = JSON.parse(r);
    try {
      chatStore[chat.channel].push(chat);
    }
    catch(err) {
      chatStore[chat.channel] = [];
      chatStore[chat.channel].push(chat);
    }
    if (chat.channel == currentChannel) {
        insertChatItem(chat);
    }
    // 添加浏览器 push
    let title = '收到新消息'
    let body = `<${chat.channel}>: ${chat.content}`
    Push.create(title, {
        body: body,
        icon: {
            x16: 'images/icon-x16.png',
            x32: 'images/icon-x32.png'
        },
        timeout: 10000
    })
};


var subscribe = function () {
    // var sse = new EventSource("/chat/subscribe");
    // sse.onmessage = function (e) {
    //     log(e, e.data);
    //     chatResponse(e.data);
    // };

    socket.on('message', function(data) {
      chatResponse(JSON.stringify(data));
    });
};

var bindToggleReaction = function() {
  socket.on('response_toggle_reaction', function(data) {
    console.log(data);
    var chat = $(`[data-id=${data.chat_id}]`)
    console.log(chat);
    var reaction = chat.find(`div[data-emoji-id=${data.emoji_id}]`)
    // if (reaction.length > 0) {
    //   reaction.find('.reaction-nums').html();
    //   var n = reaction.find('.reaction-nums').html();
    //   reaction.find('.reaction-nums').html(parseInt(n) + 1);
    //   console.log(6666);
    // } else {
    //   var t = `
    //   <div class=inline-block data-emoji-id=${data.emoji_id}>
    //     ${ReactionSington.render(data.emoji_id)}
    //     <span class='reaction-nums'>1</span>
    //   </div>
    //   `
    //   // var t = ReactionSington.render(data)
    //   currentChat.find('.chat-reaction-list').append(t)
    // }
    if (data.status == 'add') {
      if (reaction.length > 0) {
        reaction.find('.reaction-nums').html();
        var n = reaction.find('.reaction-nums').html();
        reaction.find('.reaction-nums').html(parseInt(n) + 1);
        console.log(6666);
      } else {
        var t = `
        <div class=inline-block data-emoji-id=${data.emoji_id}>
          ${ReactionSington.render(data.emoji_id)}
          <span class='reaction-nums'>1</span>
        </div>
        `
        // var t = ReactionSington.render(data)
        currentChat.find('.chat-reaction-list').append(t)
      }
    } else {
      reaction.find('.reaction-nums').html();
      var n = reaction.find('.reaction-nums').html();

      console.log(reaction);
      console.log(reaction.find('.reaction-nums'));
      console.log(parseInt(n) - 1);
      reaction.find('.reaction-nums').html(parseInt(n) - 1);
      console.log(2333);
    }
  });
}

var sendMessage = function () {
    // var name = $('#id-input-name').val();
    var content = $('#id-input-content').val();
    var message = {
        // username: name,
        content: content,
        channel: currentChannel,
    };

    // var request = {
    //     url: '/chat/add',
    //     type: 'post',
    //     contentType: 'application/json',
    //     data: JSON.stringify(message),
    //     success: function (r) {
    //         log('success', r);
    //     },
    //     error: function (err) {
    //         log('error', err);
    //     }
    // };
    // $.ajax(request);

    // websocket
    // socket.emit('text', message);
    socket.emit('text', message);
    $("#id-input-content").val("");

};

var changeChannel = function (channel) {
    document.title = '聊天室 - ' + channel;
    $('#currentChannel').html('聊天室 - ' + channel);
    currentChannel = channel;
};

var currentChat;

var bindActions = function () {
    $('#id-button-send').on('click', function () {
        // $('#id-input-content').val();
        sendMessage();
        return false;
    });
    $('#historyMessage').on('click', function () {
      window.open(`/channel/${currentChannel}/chats/0`)
    })
    $(document).keydown(function(event) {
      if(event.keyCode == 13) {
        sendMessage();
      }
    })
    // 频道切换
    $('.rc-channel').on('click', 'a', function (e) {
        e.preventDefault();
        var channel = $(this).text();
        changeChannel(channel);
        // 切换显示
        // $('.rc-channel').removeClass('active');
        // $(this).closest('.rc-channel').addClass('active');
        // reload 信息
        $('#main').find('.chat-item').remove();
        var chats = chatStore[currentChannel];
        insertChats(chats);
        return false;
    })
    $('#main').on('mouseenter', '.chat-item', function() {
      if ($(this).find('.reaction').length > 0) {
        return false;
      }
      currentChat = $(this)
      var t = `
      <div class="reaction">
      </div>`
      $(this).append(t)
      var data = {
        selector: '.reaction',
        func: toggleReaction,
      }
      ReactionSington.new(data)
      return false;
    })
    $('#main').on('mouseleave', '.chat-item', function() {
      $(this).find('.reaction').remove()
      return false;
    })


};

// long time ago
var longTimeAgo = function () {
    var timeAgo = function (time, ago) {
        return Math.round(time) + ago;
    };

    $('time').each(function (i, e) {
        var past = parseInt(e.dataset.time);
        var now = Math.round(new Date().getTime() / 1000);
        var seconds = now - past;
        var ago = seconds / 60;
        // log('time ago', e, past, now, ago);
        var oneHour = 60;
        var oneDay = oneHour * 24;
        // var oneWeek = oneDay * 7;
        var oneMonth = oneDay * 30;
        var oneYear = oneMonth * 12;
        var s = '';
        if (seconds < 60) {
            s = timeAgo(seconds, ' 秒前')
        } else if (ago < oneHour) {
            s = timeAgo(ago, ' 分钟前');
        } else if (ago < oneDay) {
            s = timeAgo(ago / oneHour, ' 小时前');
        } else if (ago < oneMonth) {
            s = timeAgo(ago / oneDay, ' 天前');
        } else if (ago < oneYear) {
            s = timeAgo(ago / oneMonth, ' 月前');
        }
        $(e).text(s);
    });
};

function api(url) {
  var url = url;
  var xhr = new XMLHttpRequest();
  var result;
  var p = new Promise(function (resolve, reject) {
    xhr.open('POST', url, true);
    xhr.onload = function (e) {
      if (this.status === 200) {
        result = JSON.parse(this.responseText);
        console.log(result);
        resolve(result);
      }
    };
    xhr.onerror = function (e) {
      reject(e);
    };
    xhr.send();
  });
  return p;
}

function emojiCallback(data) {
  var input = $('#id-input-content')
  var content = input.val() + data
  input.val(content)
}

function reactionCallback(data) {
  var emoji_id = data.replace(/:/g, '')
  var reaction = currentChat.find(`div[data-emoji-id=${emoji_id}]`)
  if (reaction.length > 0) {
    reaction.find('.reaction-nums').html();
    var n = reaction.find('.reaction-nums').html();
    reaction.find('.reaction-nums').html(parseInt(n) + 1);
    console.log(6666);
  } else {
    var t = `
    <div class=inline-block data-emoji-id=${emoji_id}>
      ${ReactionSington.render(data)}
      <span class='reaction-nums'>1</span>
    </div>
    `
    // var t = ReactionSington.render(data)
    currentChat.find('.chat-reaction-list').append(t)
  }
  console.log(currentChat.find(`div[data-emoji-id=${emoji_id}]`));
}
function toggleReaction(data) {
  var emoji_id = data.replace(/:/g, '')
  var chat_id = currentChat.data('id')
  var message = {
    emoji_id: emoji_id,
    chat_id: chat_id,
  }
  socket.emit('toggle_reaction', message);
}


var __main = function () {
    initChatStore();
    subscribe();
    bindToggleReaction();
    bindActions();
    // 选中第一个 channel 作为默认 channel
    $('.rc-channel').eq(0).find('a').click();
    currentChannel = $('.rc-channel').eq(0).find("a").text();

    // 更新时间的函数
    setInterval(function () {
        longTimeAgo();
    }, 1000);
};

$(document).ready(function () {
    __main();
});
