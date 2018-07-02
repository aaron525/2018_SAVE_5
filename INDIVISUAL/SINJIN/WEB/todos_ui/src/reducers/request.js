import rp from 'request-promise'

const apiList = function () {
  let _data = {}
  const options = {
    url: "http://localhost:3000/api/list",
    json: true,
    method: 'GET'
  }
  rp(options)
    .then(function (data) {
      _data = data;
    })
    .catch(function (err) {
      console.log('catch', err);
    });
  return _data
}

const apiItem = function (_qs) {
  let _data = {}
  const options = {
    url: "http://localhost:3000/api/item",
    json: true,
    method: 'POST',
    body: { "body": _qs["obj"] }
  }
  rp(options)
    .then(function (data) {
      _data = data;
    })
    .catch(function (err) {
      console.log('catch', err);
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
