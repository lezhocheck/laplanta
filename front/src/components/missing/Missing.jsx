import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import styles from './Missing.module.scss';
import {TbMoodCry} from 'react-icons/tb';
import Button from 'react-bootstrap/Button';
import {Link} from 'react-router-dom';

const Missing = () => {
    return (
        <Container className={styles.wrapper}>
            <Row>
                <Col>
                    <TbMoodCry className="text-light" size={500}/>
                </Col>
                <Col>
                    <Container className={styles.container}>
                        <h1 className='text-light' style={{fontSize: '10rem'}}>Oops!</h1>
                        <h5 className='text-light'>Page you are looking for does not exist</h5>
                    </Container>
                </Col>
            </Row>
            <Row>
                <Col className={styles.button}>
                    <Button variant="outline-light">
                        <Link to='/' className='text-light' style={{textDecoration: 'none'}}>Go home</Link>
                    </Button>
                </Col>
            </Row>
        </Container>
    );
}

export default Missing;