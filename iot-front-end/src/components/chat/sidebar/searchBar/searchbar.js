import React from 'react';
import { Input } from 'antd';
import './searchbar.css';
import 'antd/dist/antd.css';

const { Search } = Input;

const SearchBar = ()=> {
    return (
        <div className='searchbox'>
            <Search placeholder="input search text" enterButton />
        </div>
    )
}

export default SearchBar;