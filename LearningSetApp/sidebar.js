var categories = JSON.parse(localStorage.getItem('categories'))
console.log(categories)

render()

document.getElementById('add').onclick = function(){
  let n = document.getElementById('input').value
  categories.push(n)
  localStorage.setItem('categories', JSON.stringify(categories))
  render()
  document.getElementById('input').value = ""
}

document.getElementById('reset').onclick = function(){
  reset()
}

document.getElementById('save').onclick = function(){
  save()
}

document.getElementById('export').onclick = function(){
  file()
}

function render(){
  document.getElementById('category').innerHTML = ''
  categories = JSON.parse(localStorage.getItem('categories'))
  for(i=0; i<categories.length; i++){
    var tag = document.createElement("option");
    var node = document.createTextNode(categories[i]);
    tag.appendChild(node)
    document.getElementById('category').appendChild(tag)
  }
}

function save(){
  let saves = JSON.parse(localStorage.getItem('saves')) || []
  let n = {
    category: document.getElementById('category').value,
    code: document.getElementById('code').value
  }
  saves.push(n)
  localStorage.setItem('saves', JSON.stringify(saves))
  document.getElementById('code').value = ''
}

function reset(){
  // resets the local store containing the categories
  localStorage.setItem('categories', JSON.stringify([]))
  render()
}

function file(){
  const data = localStorage.getItem('saves')
  var file = new File([data], {type: "text/plain;charset=utf-8"});
  saveAs(file, "chrome-element-sorter-export.txt");
}
