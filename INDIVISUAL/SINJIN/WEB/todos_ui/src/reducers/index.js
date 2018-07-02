import { combineReducers } from 'redux'
import todos from './todos'
import request from './request'
import visibilityFilter from './visibilityFilter'

const todoApp = combineReducers({
  request,
  todos,
  visibilityFilter
})

export default todoApp
