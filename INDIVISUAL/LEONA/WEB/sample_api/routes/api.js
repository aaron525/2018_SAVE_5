const express = require('express');
const fs = require('fs');
const router = express.Router();

const dataFile = "./data/data.json";
const defaultChar = "utf8";
const results = {
  "code" : {
    "success": "200",
    "error": "1"
  },
  "message" : {
    "success": "success request",
    "error": "id error!!"
  }
};

const getResultCode = function(_type) {
  return JSON.stringify({"resultCode":results.code[_type], "message":results.message[_type]});
};

const getList = function(req, res) {
  fs.readFile(dataFile, defaultChar, function(err, data) {
    return res.send(data === "" ? {} : data);
  })
};

const postItem = function(req, res) {
  fs.readFile(dataFile, defaultChar, function(err, data) {
    var body = req.body.body;
    var oldTodos = data === "" ? {} : JSON.parse(data);
    var tempId = body.id === "" ? 0 : body.id;

    const getQs = function(_id){
      return JSON.stringify(
        oldTodos[String(_id)] = {
          "completed": body.completed,
          "text": body.text
        }
      )
    }

    if (body.id === "") {
      // add item
      if (Object.keys(oldTodos).length > 0) {
        Object.keys(oldTodos).forEach(function(k) {
          if (Number(k) >= tempId) {
            tempId = Number(k) + 1;
          }
        });
      }
    } else {
      // modify item
      if (!oldTodos[String(body.id)]) {
        return res.send(getResultCode('error'));
      }
    }

    fs.writeFile(dataFile, getQs(tempId), defaultChar, function(err) {
      if (err) throw err;
      console.log("save complete!");

      return res.send(getResultCode('success'));
    });
    // writeFile(getQs(tempId));
  });
};

router.get('/list', getList)
.post('/item', postItem);

module.exports = router;
