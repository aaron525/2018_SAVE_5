import React from 'react'
import { connect } from 'react-redux'
import rp from 'request-promise'
import { addTodo, apiItem } from '../actions'


let AddTodo = ({ dispatch }) => {
  let input

  const options = {
    url : "http://localhost:3000/api/list",
    json: true,
    method: 'GET'
  }
  rp(options)
    .then(function (data) {
      for(var key in data){
        dispatch(addTodo(data[key].text), key)
      }
    })
    .catch(function (err) {
      console.log('catch',err);
    });

  return (
    <form className="container"
      onSubmit={e => {
      e.preventDefault()
      if (!input.value.trim()) {
        return
      }
      dispatch(addTodo(input.value,""))
      dispatch(apiItem({"text":input.value,"completed":false,"id":""}))

      input.value = ''
    }}>
      <div className="row">
        <div className="input-group">
          <input ref={node => {
            input = node
          }}
            className="form-control border border-primary"
          />
          <div className="input-group-append">
            <button type="submit"
              className="btn btn-primary">
              Add Todo
            </button>
          </div>
        </div>
      </div>
    </form>
  )
}
AddTodo = connect()(AddTodo)

export default AddTodo
