const todos = (state = [], action) => {
  switch (action.type) {
    case 'ADD_TODO':
      const data = {
        id: action.id,
        text: action.text,
        completed: false,
      };
      return [
        ...state,
        data
      ]
    case 'TOGGLE_TODO':
      return state.map(todo =>
        (todo.id === action.id)
          ? { ...todo, completed: !todo.completed }
          : todo
      )
    default:
      return state
  }
}

export default todos
