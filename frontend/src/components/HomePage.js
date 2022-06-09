import React, { Component, useState, useEffect } from "react";
import RoomJoinPage from "./RoomJoinPage";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  Redirect,
  useParams,
} from "react-router-dom";
import Button from "@mui/material/Button"
import { Alert, ButtonGroup } from "@mui/material";
import Grid from "@mui/material/Grid"
import Typography from "@mui/material/Typography"
import { Collapse } from '@mui/material';
import IconButton from '@mui/material/IconButton';
import CircularProgress from '@mui/material/CircularProgress';
import Cookies from 'js-cookie'
import Accordion from '@mui/material/Accordion';
import AccordionDetails from '@mui/material/AccordionDetails';
import AccordionSummary from '@mui/material/AccordionSummary';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';



/**
 * Página principal del front
 * Maneja las request al backend
 * construye la interfaz
 */

export default function HomePage() {

  /**
   * Constantes
   * State - spotifyAuthenticated -> Estado de autenticación del usuario
   * State - errorMgs -> Muestra los errores
   * State - successMsg -> Maneja los mensajes de exito en las operaciones
   * State - creating -> Maneja el mensaje de que se está creando la playlist, esperando respuesta del back
   */


    const [spotifyauthenticated, setSpotifyauthenticated] = useState(false);
    const [errorMsg, setErrorMsg] = useState("");
    const [successMsg, setSuccessMsg] = useState("");
    const [creating, setCreating] = useState(false);

    let auth = useParams();

    /**
     * Llama función en el backend que revisa si el usuario está autenticado en Spotify
     * en el caso que no lo esté lo redirije a Spotify
     */
    const authenticateSpotify = async () => {
      fetch("/spotify/is-authenticated")
        .then((response) => response.json())
        .then((data) => {
          setSpotifyauthenticated(data.status);
         
          if (!data.status) {
            fetch("/spotify/get-auth-url")
              .then((response) => response.json())
              .then((data) => {
                window.location.replace(data.url);
              });
          }
          setSuccessMsg(" Has iniciado sesión correctamente - Ya puedes recibir tu contrarecomendación")
        });   
    }

    /**
     * Llama la función de crear playlist en el backend
     */

    const createPlaylist = async () => {
      setCreating(true)
      fetch("/spotify/createplaylist").then((response) => {
        console.log(response)
        setCreating(false)
        if (response.ok) {
          setSuccessMsg( "Playlist creada!")
          };
        if (!response.ok){
          setErrorMsg("upsidipsi pasó algo inexperado y no se creo la playlist, intenta de nuevo!");
        }
      });
    }

    /**
     * Revisa si el usuario tiene una sesión abierta con el backend
     */
    const getStatus = async () => {
      fetch("/spotify/getsessionid").then((response) => {
        if (response.status === 302) {
          setSpotifyauthenticated(true)
          };
      });



    }

    /**
     * Llama la función getStatus() cada vez que la página se carga
     * De esta forma, es posible comprobrar si el usuario ya está logeado en Spotify y en el Backend de forma automática
     */

    useEffect(()=> {

      console.log("Hola esto se corrió")
      getStatus()

      
      }, [])

    /**
     * Render de React
     */
    return (
      <>
      <div id="spotify">
          <Collapse in={successMsg!== ""}>
          <Alert  severity="success"
          action={
            <IconButton
              aria-label="close"
              color="inherit"
              size="small"
              onClick={() => {
                setSuccessMsg("")
              }}
            >
              x
            </IconButton>
          }
          sx={{ mb: 2 }}
        >
          {successMsg}
        </Alert>
          </Collapse>
          <Collapse in={ errorMsg !== ""}>
          <Alert  severity="error"
          action={
            <IconButton
              aria-label="close"
              color="inherit"
              size="small"
              onClick={() => {
                setErrorMsg("")
              }}
            >
              x
            </IconButton>
          }
          sx={{ mb: 2 }}
        >
          {errorMsg}
        </Alert>
          </Collapse>
          </div>
          <div className="content">
            <div className="info">
            <h2>Generador de contrarecomendaciones en Spotify</h2>
            </div>
            <Collapse in={!spotifyauthenticated}>

            
            <div className="info"><p>Para iniciar inicia sesión en Spotify dando click acá</p>
            <Button color="primary" onClick={(authenticateSpotify)}>
              Login en Spotify
          </Button>
          </div>
          </Collapse>
          <Collapse in={spotifyauthenticated}> 

      <div className="info"><p>
        Al dar click se creará una contrarecomendación como 
        una playlist en tu cuenta.
        </p>
        <p>
        Hemos usado información de tu cuenta de 
        Spotify para recomendarte música con factores aleatorios
        </p>
      <Button color="secondary" onClick={(createPlaylist)}>
              Crear Playlist
            </Button>
      
          </div>
      </Collapse>
      <Collapse in={creating}>
        <div className="info">
        <CircularProgress /><p>Contrarecomendando</p>
        </div>
      
          </Collapse>

          <div id="sobre" class="info">
          <h2>Burbujas estéticas y contra-recomendaciones </h2>
          <p>Este proyecto de investigación-creación se centra en lo que llamo <b>burbujas estéticas</b>, un fenómeno que se produce en espacios o plataformas de consumo de objetos estéticos donde, por la interferencia de un agente infomediario, se produce reducción de la diversidad de consumo de objetos estéticos</p>
          <h3>Cómo funciona</h3>
          <ul>
          <li> selecciona un artista de forma aleatoria  de los 20 artistas favoritos del usuario</li>
          <li> se toman 20 artistas relacionados a este primer artista</li>
          <li> se agregan 4 canciones del top de canciones de los artistas seleccionados</li>
          <li> En caso que el usuario no tenga ningún artista en su top de artistas se hace una búsqueda con una letra aleatoria y se selecciona un artista al azar de esa búsqueda.</li>
          </ul>
          <p>En este último paso hay un sesgo, Spotify solo devuelve los artistas más populares</p>

          <p>El objetivo de este algoritmo es generar recomendaciones paralelas, mas no generar mejores recomendaciones que Spotify</p>

          <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1a-content"
          id="panel1a-header"
        >
          <Typography>Sobre las Burbujas Estéticas</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>
          Las burbujas estéticas son una estructura que se produce en los espacios o plataformas de consumo de objetos estéticos donde, por la interferencia de un agente infomediario, los usuarios son expuestos mayormente a objetos estéticos que consumen actualmente o que son similares a este y, como consecuencia, se produce una reducción en la diversidad del consumo de música. 
          </Typography>
        </AccordionDetails>
      </Accordion>
      <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel2a-content"
          id="panel2a-header"
        >
          <Typography>Sistema de Recomendación</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>
          Un sistema de recomendación (SR) consiste en usar fuentes de información y datos para inferir los intereses del usuario, que en el caso de Spotify no son solamente los intereses, sino también el gusto de los usuarios.
          </Typography>
        </AccordionDetails>
      </Accordion>
      <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel3a-content"
          id="panel3a-header"
        >
          <Typography>Algoritmo Curador</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>
          El algoritmo de Spotify tiene  la función de elegir qué ítems son mostrados a cada usuario, y le permiten organizar y jerarquizar los contenidos para su consumo. Así como un curador decide las obras y el orden que tienen unas obras de arte en una sala de exposición, el SR de Spotify decide qué canciones y en qué orden son recomendadas. 
          </Typography>
        </AccordionDetails>
      </Accordion>

      <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel4a-content"
          id="panel4a-header"
        >
          <Typography>Algoritmo Portero</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>
          El algoritmo de Spotify decide que objetos estéticos son considerados para generar las recomendaciones a los usuarios. No todos las canciones de Spotify se tienen en cuenta para todos los usuarios. Por esta razón, El algoritmo es un portero de los objetos estéticos en Spotify.
          </Typography>
        </AccordionDetails>
      </Accordion>
      <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel5a-content"
          id="panel5a-header"
        >
          <Typography>Algoritmo como Infomediario</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>
         El sistema de recomendación de Spotify media la experiencia entre los productores y los consumidores de contenido. Así mismo Morris menciona ( 2015b, p.  447)*, que los algoritmos de recomendación logran crear audiencias basadas en los datos y la información que tienen de los usuarios. 

         *revisar la cita en el texto, link disponible pronto
          </Typography>
        </AccordionDetails>
      </Accordion>

          
          <h3>Preguntas finales</h3>
          <p>¿Qué elementos usa Spotify para generar las recomendaciones?</p>
          <p>¿Cómo se pueden evitar los sesgos de los algoritmos?</p>
          <p>¿Qué papel tienen los otros agentes de la industria de la música en las recomendaciones?</p>
          <p>¿Cómo podemos mejorar el algoritmo para que permita que se descubra música nueva?</p>
          <p>¿Cómo afecta el Sistema de recomendación de Spotify la creación de música?</p>
          <p>Si tienes respuestas a estas preguntas o más preguntas me las puedes enviar a felipe(at)felipesalas.com</p>
          
          <h5>El documento teórico sobre las burbujas estéticas y esta aplicación será publicado pronto</h5>
          <Button disabled variant="outlined">Ver el texto</Button>
          </div>
        
        
        
        </div>

      
    
      </>
    );
  
}