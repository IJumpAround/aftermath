import React, {Component} from "react";
import ItemTable from './ItemTable'
import axios from "../../utils/axiosInstance";


class FilterableItemTable extends Component {
    constructor(props) {
        super(props);
        this.state = {data: {}}
    }

    async componentDidMount() {
        let response;
        try {
            response = await axios.get("items/");
            this.setState({data: response.data})
        } catch (e) {
            console.log('error {}', e)
        }
    }

    render() {
        if(this.state.data) {
            return (<div>
                {JSON.stringify(this.state.data)}
            </div>)
        } else {
            return <div>Nothing to see here</div>
        }

   }
}


export default FilterableItemTable;