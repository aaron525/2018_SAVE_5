import React from 'react'
import FilterLink from '../containers/FilterLink'

const Footer = () => (
  <div className="container">
    <div className="row">
      <div className="col-sm">
        <FilterLink filter="SHOW_ALL">
          Show All
        </FilterLink>
      </div>
      <div className="col-sm">
        <FilterLink filter="SHOW_ACTIVE">
          Active
        </FilterLink>
      </div>
      <div className="col-sm">
        <FilterLink filter="SHOW_COMPLETED">
          Completed
        </FilterLink>
      </div>
    </div>
  </div>
)

export default Footer
