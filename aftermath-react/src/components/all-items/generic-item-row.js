import React from "react";
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faCheckSquare} from "@fortawesome/free-solid-svg-icons";
import {faSquare} from "@fortawesome/free-regular-svg-icons";

function BasicItemRow(props) {
    let item = props.item;
    let item_type = item.model_type;
    let item_id = item.id;
    const requiresAttunement = (item.requires_attunement === true) ? faCheckSquare : faSquare
    console.log(`props:`,props)
    return (
        <tr>
            <td><a href={`/${item_type}/${item_id}`}>{item.name}</a></td>
            <td>{item.rarity}</td>
            <td>{item.wondrous}</td>
            <td> <FontAwesomeIcon icon={requiresAttunement}/> </td>
            <td>{item.player}</td>
            <td>{item.quantity }</td>

        </tr>
    )
}

export default BasicItemRow;