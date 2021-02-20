function updatePresence(tab) {
  var re = RegExp("(http|https):\/\/(.*).dcinside.(co.kr|com)\/.*");
  if (tab && re.test(tab.url)) {
    var data = {
      action: "set",
      details: String(tab.title).split(' - ').reverse()[0],
      state: tab.title
    };
  } else {
    var data = {
      action: 'clear'
    }
  }

  var settings = {
    "async": true,
    "crossDomain": true,
    "url": "http://localhost:27328/",
    "method": "POST",
    "headers": {
      "content-type": "application/json"
    },
    "processData": false,
    "data": JSON.stringify(data)
  }

  $.ajax(settings);
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

var Last;
setInterval(function () { // on an interval…
  chrome.windows.getLastFocused({populate: true}, function (window) { // get the last focused window
    if (window.focused) {
      if (window.tabs)
        for (let tab of window.tabs)
          if(Last != tab.url) {
            if (tab.highlighted) {
              updatePresence(tab);
              Last = tab.url;
              break;
            }
          }
    }
  });
}, 1000);