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
    var type = chat.type
    var name = chat.username;
    var avatar = chat.avatar;

    if (type == 'join') {
        var t = `
            <div>
                <img src="${avatar}"  height="10" width="10" class="avatar__image" alt="">
                <span>${name} 加入了聊天</span>
            </div>
        `
    } else {
        var content = chat.content;
        content = filterEmoji(content)
        var time = chat.created_time;
        var t = `
        <div class="chat-item burstStart read burstFinal">
            <div class="chat-item__container">
                <div class="chat-item__aside">
                    <div class="chat-item__avatar">
                        <span class="widget">
                            <div class="trpDisplayPicture avatar-s">
                                <img src="${avatar}"  height="30" width="30" class="avatar__image" alt="">
                            </div>
                        </span>
                    </div>
                </div>
                <div class="chat-item__actions js-chat-item-actions">
                    <i class="chat-item__icon icon-check chat-item__icon--read chat-item__icon--read-by-some js-chat-item-readby"></i>
                    <i class="chat-item__icon icon-ellipsis"></i>
                </div>
                <div class="chat-item__content">
                    <div class="chat-item__details">
                        <div class="chat-item__from js-chat-item-from">${name}</div>
                        <a class="chat-item__time js-chat-time" href="#">
                            <time data-time="${time}"></time>
                        </a>
                    </div>
                    <div class="chat-item__text js-chat-item-text">${content}</div>
                </div>
            </div>
        </div>
        `;
      var staticFileURLPreix = location.origin + '/static/'
      var new_t = `<div class="chat-item">
                      <div class="user">
                          <div class="user-avatar"><img src="${staticFileURLPreix + avatar}" class="user-avatar"></div>
                          <div class="user-info">
                              <div class="user-name">${name}</div>
                              <div class="pass-time" href="#">
                                  <time data-time="${time}"></time>
                              </div>
                          </div>
                      </div>
                      <div class="user_content">
                          ${content}
                      </div>
                  </div>`
    }

    return new_t;
};

var insertChats = function (chats) {
    var selector = '#main'
    var chatsDiv = $(selector);
    var html = chats.map(chatItemTemplate);
    chatsDiv.append(html.join(''));
    scrollToBottom(selector);
};

var insertChatItem = function (chat) {
    var selector = '#main'
    var chatsDiv = $(selector);
    var t = chatItemTemplate(chat);
    chatsDiv.append(t);
    scrollToBottom(selector);
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
};



var __main = function () {
    subscribe();
    bindActions();
    // 选中第一个 channel 作为默认 channel
    // $('.rc-channel')[0].click();
    currentChannel = $('.rc-channel').eq(0).find("a").text();
    initChatStore();
    // 更新时间的函数
    setInterval(function () {
        longTimeAgo();
    }, 1000);
};

$(document).ready(function () {
    __main();
});
