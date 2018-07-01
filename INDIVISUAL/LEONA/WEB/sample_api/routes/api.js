const express = require('express')
const cors = require('cors')
const fs = require('fs')
const router = express.Router()
const app = express()
app.use(cors())

const dataFile = './data/data.json'
const defaultChar = "utf8"
const results = {
  "code" : {
    "success": "100",
    "error": "1"
  },
  "message" : {
    "success": "success",
    "error": "id error!!"
  }
}

const getResultCode = function(_type){
  return JSON.stringify({"resultCode":results.code[_type],"message":results.message[_type]})
}

const getReadfile = function(req, res){
  console.log(req)
  console.log(res)
  fs.readFile(dataFile, defaultChar, function(err, data) {
    return res.send( (data === "") ? {} : data )
  })
}

const postReadfile = function(req, res){
  fs.readFile(dataFile, defaultChar, function(err, data) {
    var oldTodos = (data === "") ? {} : JSON.parse(data)
    var body = req.body.body

    // add item
    var tempId = 0
    if(Object.keys(oldTodos).length > 0){
      Object.keys(oldTodos).forEach(function(k){
        if(Number(k) >= tempId){
          tempId = Number(k) + 1
        }
      })
    }

    oldTodos[String(tempId)] = {
      "id": body.id,
      "completed": body.completed,
      "text": body.text
    }

    fs.writeFile(dataFile, JSON.stringify(oldTodos), defaultChar, function(err) {
      if(err) throw err
      console.log("save complete!")

      return res.send(getResultCode('success'))
    });
  });
}

router.all('/', function(req, res, next) {
  // for cors
  res.header('Access-Control-Allow-Origin', '*')
  res.header('Access-Control-Allow-Headers', 'Accept,Authorization,Cache-Control,Content-Type,DNT,If-Modified-Since,Keep-Alive,Origin,User-Agent,X-Requested-With')
  res.append('Access-Control-Allow-Credentials', 'true');
  res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  next()
})
.get('/list', getReadfile)
.post('/item', postReadfile)

module.exports = router