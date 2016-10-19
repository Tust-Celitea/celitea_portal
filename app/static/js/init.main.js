$("#feeds-blog").rss(
  "https://blog.celitea.xyz/index.php/feed/",
  {
    // how many entries do you want?
    // default: 4
    // valid values: any integer
    limit: 6,

    // want to offset results being displayed?
    // default: false
    // valid values: any integer
    offsetStart: false, // offset start point
    offsetEnd: false, // offset end point

    // will request the API via https
    // default: false
    // valid values: false, true
    ssl: true,

    // which server should be requested for feed parsing
    // the server implementation is here: https://github.com/sdepold/feedr
    // default: feedrapp.info
    // valid values: any string
    host: 'feedparse.yoitsu.xyz',

    // outer template for the html transformation
    // default: "<ul>{entries}</ul>"
    // valid values: any string
    layoutTemplate: '<div class="collection">{entries}</div>',

    // inner template for each entry
    // default: '<li><a href="{url}">[{author}@{date}] {title}</a><br/>{shortBodyPlain}</li>'
    // valid values: any string
    entryTemplate: '<a href="{url}" class="collection-item">{title}<span class="badge">{date}</span></a>',

    // additional token definition for in-template-usage
    // default: {}
    // valid values: any object/hash
    tokens: {
      foo: 'bar',
      bar: function(entry, tokens) { return entry.title }
    },

    // formats the date with moment.js (optional)
    // default: 'dddd MMM Do'
    // valid values: see http://momentjs.com/docs/#/displaying/
    dateFormat: 'YYYY MMM Do',

    // localizes the date with moment.js (optional)
    // default: 'en'
    dateLocale: 'zh-cn',

    // formats the date in whatever manner you choose. (optional)
    // this function should return your formatted date.
    // this is useful if you want to format dates without moment.js.
    // if you don't use moment.js and don't define a dateFormatFunction, the dates will
    // not be formatted; they will appear exactly as the RSS feed gives them to you.
    //dateFormatFunction: function(date){},

    // the effect, which is used to let the entries appear
    // default: 'show'
    // valid values: 'show', 'slide', 'slideFast', 'slideSynced', 'slideFastSynced'
    effect: 'show',

    // a callback, which gets triggered when an error occurs
    // default: function() { throw new Error("jQuery RSS: url don't link to RSS-Feed") }
    //error: function(){},

    // a callback, which gets triggered when everything was loaded successfully
    // this is an alternative to the next parameter (callback function)
    // default: function(){}
    //success: function(){},

    // a callback, which gets triggered once data was received but before the rendering.
    // this can be useful when you need to remove a spinner or something similar
    //onData: function(){}
  },

  // callback function
  // called after feeds are successfully loaded and after animations are done
  function callback() {
  }
);

$("#feeds-forum").rss(
  "https://forum.celitea.xyz/feed",
  {
    // how many entries do you want?
    // default: 4
    // valid values: any integer
    limit: 6,

    // want to offset results being displayed?
    // default: false
    // valid values: any integer
    offsetStart: false, // offset start point
    offsetEnd: false, // offset end point

    // will request the API via https
    // default: false
    // valid values: false, true
    ssl: true,

    // which server should be requested for feed parsing
    // the server implementation is here: https://github.com/sdepold/feedr
    // default: feedrapp.info
    // valid values: any string
    host: 'feedparse.yoitsu.xyz',

    // outer template for the html transformation
    // default: "<ul>{entries}</ul>"
    // valid values: any string
    layoutTemplate: '<div class="collection">{entries}</div>',

    // inner template for each entry
    // default: '<li><a href="{url}">[{author}@{date}] {title}</a><br/>{shortBodyPlain}</li>'
    // valid values: any string
    entryTemplate: '<a href="{url}" class="collection-item">{title}</a>',

    // additional token definition for in-template-usage
    // default: {}
    // valid values: any object/hash
    tokens: {
      foo: 'bar',
      bar: function(entry, tokens) { return entry.title }
    },

    // formats the date with moment.js (optional)
    // default: 'dddd MMM Do'
    // valid values: see http://momentjs.com/docs/#/displaying/
    dateFormat: 'YYYY MMM Do',

    // localizes the date with moment.js (optional)
    // default: 'en'
    dateLocale: 'zh-cn',

    // formats the date in whatever manner you choose. (optional)
    // this function should return your formatted date.
    // this is useful if you want to format dates without moment.js.
    // if you don't use moment.js and don't define a dateFormatFunction, the dates will
    // not be formatted; they will appear exactly as the RSS feed gives them to you.
    //dateFormatFunction: function(date){},

    // the effect, which is used to let the entries appear
    // default: 'show'
    // valid values: 'show', 'slide', 'slideFast', 'slideSynced', 'slideFastSynced'
    effect: 'show',

    // a callback, which gets triggered when an error occurs
    // default: function() { throw new Error("jQuery RSS: url don't link to RSS-Feed") }
    //error: function(){},

    // a callback, which gets triggered when everything was loaded successfully
    // this is an alternative to the next parameter (callback function)
    // default: function(){}
    //success: function(){},

    // a callback, which gets triggered once data was received but before the rendering.
    // this can be useful when you need to remove a spinner or something similar
    //onData: function(){}
  },

  // callback function
  // called after feeds are successfully loaded and after animations are done
  function callback() {
  }
);
