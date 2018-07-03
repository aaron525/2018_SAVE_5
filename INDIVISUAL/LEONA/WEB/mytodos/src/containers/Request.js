import { connect } from 'react-redux'
import { apiItem } from '../actions'

const request = (type, filter) => {
  switch (filter) {
    case 'API_LIST':
      apiItem(input.value)
      return type
    case 'API_ITEM':
      return {}
    default:
      throw new Error('Unknown filter: ' + filter)
  }
}

const mapStateToProps = (state) => ({
  type: request(state.type, state.visibilityFilter)
})

const mapDispatchToProps = {
  onTodoClick: toggleTodo
}

const Request = connect(
  mapStateToProps,
  mapDispatchToProps
)(TodoList)

export default Request