import rp from 'request-promise'

const BASE_URL = 'http://localhost:3000/api'

const apiList = function () {
  let _data = {}
  const options = {
    url: BASE_URL + "/list",
    json: true,
    method: 'GET'
  }
  rp(options)
    .then(function (data) {
      _data = data;
    })
    .catch(function (err) {
      console.log('REST API Error', err);
    });
  return _data
}

const apiItem = function (_qs) {
  let _data = {}
  const options = {
    url: BASE_URL + "/item",
    json: true,
    method: 'POST',
    body: { "body": _qs["obj"] }
  }
  rp(options)
    .then(function (data) {
      _data = data;
    })
    .catch(function (err) {
      console.log('REST API Error', err);
    });
  return _data
}

const request = (state = [], action) => {
  switch (action.type) {
    case 'API_LIST':
      return [
        ...state,
        apiList()
      ]
    case 'API_ITEM':
      return [
        ...state,
        apiItem(action)
      ]
    default:
      return state
  }
}

export default request
