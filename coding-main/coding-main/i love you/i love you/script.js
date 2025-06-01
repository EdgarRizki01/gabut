//reset animations
setInterval(()=>{
  let el = document.getElementById('love')
  var newone = el.cloneNode(true);
  el.parentNode.replaceChild(newone, el);
}, 4000)
