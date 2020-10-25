import React, {Component} from "react";
import axios from "../../utils/axiosInstance";
import BootstrapTable from "react-bootstrap-table-next"
// import ToolkitProvider, {Search} from 'react-bootstrap-table-next'
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCheckSquare} from "@fortawesome/free-solid-svg-icons";
import {faSquare} from "@fortawesome/free-regular-svg-icons";
import ToolkitProvider, { Search } from 'react-bootstrap-table2-toolkit';
import paginationFactory from 'react-bootstrap-table2-paginator';
import 'react-bootstrap-table-next/dist/react-bootstrap-table2.min.css';
import 'react-bootstrap-table2-paginator/dist/react-bootstrap-table2-paginator.min.css';
import './FilterableItemTable.css'


class FilterableItemTable extends Component {
    constructor(props) {
        super(props);
        this.state = {
            items: [{}],
            ordering: 'name'
        }
    }

    async getItemList() {
        let response;
        try {
            response = await axios.get("items/", {params: {'order_by': this.state.ordering}});
            this.setState({items: response.data.resources.data})
        } catch (e) {
            console.log('error {}', e)
        }
    }

    async componentDidMount() {
        await this.getItemList()
    }

    attunementFormatter(cell) {
        const requiresAttunement = (cell === true) ? faCheckSquare : faSquare
            return (
                <span>
            <FontAwesomeIcon icon={requiresAttunement}/>
                </span>
            )
    }

    nameFormatter(cell, row) {
        const itemType = row.model_type;
        const id = row.id;

        const slug = `${itemType}/${id}`;
        return (<span><a href={slug}>{cell}</a></span>)
    }

    nameHeaderFormatter(column, colIndex, {sortElement, filterElement}) {
        return (
            <span>
                {filterElement}{column.text}{sortElement}
            </span>
        )
    }



    render() {
        const { SearchBar } = Search;
        const columns = [{
            dataField: 'name',
            text: 'Name',
            sort: true,
            formatter: this.nameFormatter,
            headerFormatter: this.nameHeaderFormatter
        }, {
            dataField: 'rarity',
            text: 'Rarity'
        }, {
            dataField: 'requires_attunement',
            text: 'Requires Attunement',
            formatter: this.attunementFormatter
        }, {
            dataField: 'player',
            text: 'Owner',
            sort: true,
        }, {
            dataField: 'quantity',
            text: 'Quantity',
        }
        ]

        if(this.state.items) {
            return (<div>
                <ToolkitProvider
                                 bootstrap4
                                 keyField='name'
                                 data={this.state.items}
                                 columns={columns}
                                 search


                >{
                    props => (
                    <div className='row'>
                        <div className='col-12'>
                            <h3>Search all items:</h3>
                            <SearchBar { ...props.searchProps } />
                            <hr />
                            <BootstrapTable bootstrap4
                                            hover
                                { ...props.baseProps }
                                            pagination = {paginationFactory()}
                            />
                         </div>
                     </div>
                    )
                }
                </ToolkitProvider>
            </div>)
        } else {
            return <div>Nothing to see here</div>
        }

   }
}


export default FilterableItemTable;