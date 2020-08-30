import React, {Component} from 'react';
import logo from './logo.svg';
import './App.css';
import 'react-bootstrap/dist/react-bootstrap'
import 'react-bootstrap/dist/react-bootstrap.min'
import 'bootstrap/dist/css/bootstrap.min.css'

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
                <header className="App-header">
                    <img src={logo} className="App-logo" alt="logo"/>
                    <p>
                        Edit <code>src/App.js</code> and save to reload.
                    </p>
                    <a
                        className="App-link"
                        href="https://reactjs.org"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        Learn React
                    </a>
                    <a className="App-link"
                       href="http://127.0.0.1:8000/admin"
                       target="_blank"
                       rel="noopener noreferrer">Admin</a>
                </header>
                <FilterableItemTable data={this.test}/>
            </div>
        );
    }
}


function getItems() {
    axios.get("/items")
}
export default App;
