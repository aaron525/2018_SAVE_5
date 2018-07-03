import React from 'react'
import Footer from './Footer'
import AddTodo from '../containers/AddTodo'
import VisibleTodoList from '../containers/VisibleTodoList'

const App = () => (
  <div className="container">
    <div className="row">
      <div className="col-9">
        <h1>My TodoList Homework</h1>
      </div>
    </div>
    <div className="row">
      <div className="col-3">
        <Footer />
      </div>
      <div className="col-6">
        <AddTodo />
        <VisibleTodoList />
      </div>
    </div>
  </div>
)

export default App
