(function() {
  var global = window;
  var href =
    global.document.location.protocol === 'https:' && 'https://db2041bd.ngrok.io' ||
    global.document.location.protocol === 'http:' && 'http://db2041bd.ngrok.io'
  global.endpointOrigin = href
}())
