const express = require('express')
const fs = require('fs')
const router = express.Router()

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
  fs.readFile(dataFile, defaultChar, function(err, data) {
    return res.send( (data === "") ? {} : data )
  })
}

const postReadfile = function(req, res){
  fs.readFile(dataFile, defaultChar, function(err, data) {
    var oldTodos = (data === "") ? {} : JSON.parse(data)
    var body = req.body.body

    if(body.id===""){
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
        "completed": body.completed,
        "text": body.text
      }
    } else {
      // modify item
      if(!oldTodos[String(body.id)]){
        return res.send(getResultCode('error'))
      }
      
      oldTodos[String(body.id)] = {
        "completed": body.completed,
        "text": body.text
      }
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
  res.header("Access-Control-Allow-Origin", "*")
  res.header("Access-Control-Allow-Headers", "X-Requested-With")
  next()
})
.get('/', getReadfile)
.post('/', postReadfile)

module.exports = router