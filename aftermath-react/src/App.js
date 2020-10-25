import React, {Component} from 'react';
import logo from './logo.svg';
import './App.css';
import 'react-bootstrap/dist/react-bootstrap'
import 'react-bootstrap/dist/react-bootstrap.min'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min'

import FilterableItemTable from "./components/all-items/FilterableItemTable";

import axios from "./utils/axiosInstance"

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {data: []}

        this.test = {}
    }

    async componentDidMount() {
        let response;
        try {
            console.log(process.env.REACT_APP_)
            response = await axios.get("items/");
        } catch (e) {
            console.log('error {}', e)
        }

        console.log(response)
        this.test = response.data
    }

    render() {
        return (
            <div className="App">
                <div className="container-fluid">
                    <div className='row'>
                        <div className='col-12'>
                            <a className="App-link"
                               href="http://127.0.0.1:8000/admin"
                               target="_blank"
                               rel="noopener noreferrer">Admin</a>
                        </div>
                    </div>
                    <div className='row'>
                        <div className='col-1'></div>
                        <div className='col-10'>
                            <FilterableItemTable data={this.test}/>
                        </div>
                        <div className='col-1'/>
                    </div>
                </div>
            </div>
        );
    }
}


function getItems() {
    axios.get("/items")
}
export default App;
