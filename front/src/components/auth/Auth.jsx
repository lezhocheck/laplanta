import React from 'react';
import Container from 'react-bootstrap/Container';
import {RiPlantLine} from 'react-icons/ri';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import styles from './Auth.module.scss';


const Auth = (props) => {
    const subtitle = props.subtitle;

    return (
        <div className={styles.wrapper}>
            <Container fluid className={styles.background}/>
            <div className={styles.container}>
                <Row>
                    <Col className={styles.imagecontainer}>
                        <img className={styles.image} src={require('../../static/cover.gif')} width="100%" height="100%" alt="Cover"/>
                    </Col>
                    <Col>
                        <div className='d-flex flex-row mt-2'>
                            <RiPlantLine size={50}/>
                            <span className="h1 fw-bold mb-0">Laplanta</span>
                        </div>
                        <h5 className="fw-normal my-4 pb-3" style={{letterSpacing: '1px'}}>{subtitle}</h5>
                        <div className={styles.input}>
                            {props.children}
                        </div>
                    </Col>
                </Row>
            </div>
        </div>
  );
}

export default Auth;