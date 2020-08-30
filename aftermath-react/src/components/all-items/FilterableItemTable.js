import React from "react";
import ItemTable from './ItemTable'


function FilterableItemTable(props) {

    return( <div>
        {JSON.stringify(props.data)}
    </div>)
    // return(<ItemTable props={props}/>)

}


export default FilterableItemTable;