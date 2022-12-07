import PlantTable from './PlantTable';
import {useState, useEffect} from 'react';
import useAxiosPrivate from '../../hooks/useAxiosPrivate';
import Container from 'react-bootstrap/Container';

const Plants = () => {
    const [plants, setPlants] = useState([]);
    const axiosPrivate = useAxiosPrivate();

    useEffect(() => {
        let isMounted = true;
        const controller = new AbortController();
        const getPlants = async () => {
            try {
                const response = await axiosPrivate.get('/plants', {
                    signal: controller.signal
                });
                isMounted && setPlants(response.data?.msg);
            } catch(e) {
                console.error(e);
            }
        }

        getPlants();

        return () => {
            isMounted = false;
            controller.abort();
        }
    }, []);
    

    return (
        <div className="bg-light" style={{height: 'auto'}}>
            <Container>
                <br/>
                <h1>My plants</h1>
                <br/>
                <PlantTable plants={plants}/>
            </Container>
        </div>
    );
}

export default Plants;