import React from 'react';
import "./App.scss";
import Layout from './components/layout/Layout';
import {Route, Routes} from 'react-router-dom';
import Login from './components/auth/Login';
import Home from './components/home/Home';
import Signup from './components/auth/Signup';
import Missing from './components/missing/Missing';
import RequireAuth from './components/requireauth/RequireAuth';
import Profile from './components/profile/Profile';

const App = () => {
    return (
        <Routes>
            <Route path="/" element={<Layout/>}> 
                {/* Public routes */}
                <Route path="/" element={<Home/>}/>
                <Route path="login" element={<Login/>}/>
                <Route path="signup" element={<Signup/>}/>

                {/* TODO: Protected routes */}
                <Route element={<RequireAuth/>}>
                    <Route path="profile" element={<Profile/>}/>
                </Route>

                {/* Catch all */}
                <Route path="*" element={<Missing/>}/>
            </Route>
        </Routes>
    );
}

export default App;
