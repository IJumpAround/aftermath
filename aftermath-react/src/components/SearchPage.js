import React from 'react';
import {InputGroup, Button, FormControl} from 'react-bootstrap'


function SearchBar() {
    return (
        <div>
            <InputGroup className="mb-3">
                <FormControl aria-describedby="basic-addon1"/>
                <InputGroup.Append>
                    <Button variant="outline-secondary">Button</Button>
                </InputGroup.Append>
            </InputGroup>
        </div>
    )
}

export default SearchBar;