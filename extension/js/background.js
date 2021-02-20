function updatePresence(tab = false) {
  var re = RegExp("(http|https):\/\/(.*).dcinside.(co.kr|com)\/.*");
  var data;

  if (tab) {
    if (re.test(tab.url)) {
      data = {
        action: "set",
        title: tab.title,
        url: String(tab.url)
      };
    }
  } else {
    data = {
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
var LastWindow;
var LastTab;
setInterval(function () {
  chrome.windows.getLastFocused({populate: true}, function (window) {
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

  chrome.tabs.onRemoved.addListener(function(tabid) {
    if(tabid != LastTab) {
      updatePresence();
      LastTab = tabid;
    }
  });
   
   chrome.windows.onRemoved.addListener(function(windowid) {
    if(windowid != LastWindow) {
      updatePresence();
      LastWindow = windowid;
    }
  });
}, 1000);