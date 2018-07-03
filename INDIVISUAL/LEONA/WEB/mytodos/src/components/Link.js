import React from 'react'
import PropTypes from 'prop-types'

const Link = ({ active, children, onClick }) => {
  if (active) {
    return <span className="btn btn-block btn-sm btn-secondary">{children}</span>
  }

  return (
    // eslint-disable-next-line
    <button type="button"
       className="btn btn-block btn-sm btn-outline-secondary"
       onClick={e => {
         e.preventDefault()
         onClick()
       }}
    >
      {children}
    </button>
  )
}

Link.propTypes = {
  active: PropTypes.bool.isRequired,
  children: PropTypes.node.isRequired,
  onClick: PropTypes.func.isRequired
}

export default Link
