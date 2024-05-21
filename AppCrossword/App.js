import React, { useState } from 'react';
import { StyleSheet, Text, View, Button, Image, ActivityIndicator, ScrollView, Dimensions } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import axios from 'axios';

const { width, height } = Dimensions.get('window');

export default function App() {
  const [gridImage, setGridImage] = useState(null);
  const [definitionImage, setDefinitionImage] = useState(null);
  const [matrix, setMatrix] = useState(null);
  const [definitions, setDefinitions] = useState(null);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState('welcome');

  const pickImage = async (setter) => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 1,
    });

    if (!result.canceled) {
      const uri = result.assets[0].uri;
      setter(uri);
      uploadImage(uri, setter === setGridImage ? 'grid.jpg' : 'definition.jpg');
    }
  };

  const uploadImage = async (uri, filename) => {
    const formData = new FormData();
    formData.append('file', {
      uri,
      name: filename,
      type: 'image/jpeg',
    });

    try {
      const response = await axios.post('http://192.168.1.10:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('Upload success:', response.data);
    } catch (error) {
      console.error('Upload error:', error);
    }
  };

  const processImages = async () => {
    setLoading(true);
    try {
      const gridResponse = await axios.post('http://192.168.1.10:5000/process-grid');
      const definitionResponse = await axios.post('http://192.168.1.10:5000/process-definition');
      console.log('Processing success:', gridResponse.data, definitionResponse.data);
      setMatrix(gridResponse.data.matrix_binaire);
      setDefinitions(definitionResponse.data);
      setPage('showGridAndDefinitions');
    } catch (error) {
      console.error('Processing error:', error);
    }
    setLoading(false);
  };

  const AnimalAnimation = () => {
    const [position, setPosition] = useState(0);

    React.useEffect(() => {
      const interval = setInterval(() => {
        setPosition((prev) => (prev < 100 ? prev + 1 : 0));
      }, 50);

      return () => clearInterval(interval);
    }, []);

    return (
      <View style={[styles.animal, { left: `${position}%` }]}>
        <Text>🐾</Text>
      </View>
    );
  };

  if (page === 'welcome') {
    return (
      <View style={styles.centeredContainer}>
        <Text>Welcome to the Crossword Solver App</Text>
        <Button title="Start" onPress={() => setPage('addImages')} />
      </View>
    );
  }

  if (page === 'addImages') {
    return (
      <View style={styles.centeredContainer}>
        <Text>Upload your images</Text>
        <View style={styles.buttonContainer}>
          <Button title="Pick Grid Image" onPress={() => pickImage(setGridImage)} />
          {gridImage && <Image source={{ uri: gridImage }} style={styles.image} />}
        </View>
        <View style={styles.buttonContainer}>
          <Button title="Pick Definition Image" onPress={() => pickImage(setDefinitionImage)} />
          {definitionImage && <Image source={{ uri: definitionImage }} style={styles.image} />}
        </View>
        {gridImage && definitionImage ? (
          <View>
            <Button title="Confirm" onPress={() => processImages()} />
            <Button title="Back to Welcome" onPress={() => setPage('welcome')} />
          </View>
        ) : (
          <Button title="Back to Welcome" onPress={() => setPage('welcome')} />
        )}
        {loading && <ActivityIndicator size="large" color="#00ff00" />}
      </View>
    );
  }

  if (page === 'showGridAndDefinitions') {
    return (
      <View style={styles.container}>
        <Text style={styles.title}>Here is your crossword grid and definitions:</Text>
        <View style={styles.gridAndDefinitionsContainer}>
          <View style={styles.gridContainer}>
            <Text style={styles.sectionTitle}>Crossword Grid</Text>
            <ScrollView horizontal>
              <View style={styles.matrixContainer}>
                {matrix && matrix.map((row, rowIndex) => (
                  <View key={rowIndex} style={styles.matrixRow}>
                    {row.map((cell, cellIndex) => (
                      <View
                        key={cellIndex}
                        style={[
                          styles.matrixCell,
                          { backgroundColor: cell === 1 ? 'white' : 'orange' },
                        ]}
                      />
                    ))}
                  </View>
                ))}
              </View>
            </ScrollView>
          </View>
          <ScrollView style={styles.definitionsScrollContainer}>
            <View style={styles.definitionsContainer}>
              <View style={styles.column}>
                <Text style={styles.definitionHeader}>HORIZONTALEMENT:</Text>
                {definitions && Object.keys(definitions.HORIZONTALEMENT).map((key) => (
                  <View key={key} style={styles.definitionContainer}>
                    <Text style={styles.definitionKey}>{key}</Text>
                    <Text style={styles.definitionText}>{definitions.HORIZONTALEMENT[key]}</Text>
                  </View>
                ))}
              </View>
              <View style={styles.column}>
                <Text style={styles.definitionHeader}>VERTICALEMENT:</Text>
                {definitions && Object.keys(definitions.VERTICALEMENT).map((key) => (
                  <View key={key} style={styles.definitionContainer}>
                    <Text style={styles.definitionKey}>{key}</Text>
                    <Text style={styles.definitionText}>{definitions.VERTICALEMENT[key]}</Text>
                  </View>
                ))}
              </View>
            </View>
          </ScrollView>
        </View>
        <Button title="Next" onPress={() => setPage('animalAnimation')} />
        <Button title="Back to Home" onPress={() => setPage('welcome')} />
      </View>
    );
  }

  if (page === 'animalAnimation') {
    return (
      <View style={styles.centeredContainer}>
        <Text>Solving...</Text>
        <AnimalAnimation />
        <Button title="Back to Home" onPress={() => setPage('welcome')} />
      </View>
    );
  }

  return null;
}

const styles = StyleSheet.create({
  centeredContainer: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  container: {
    flex: 1,
    backgroundColor: '#fff',
    padding: 20,
  },
  buttonContainer: {
    margin: 10,
  },
  image: {
    width: 200,
    height: 200,
    margin: 10,
  },
  gridAndDefinitionsContainer: {
    flex: 1,
    marginTop: 20,
  },
  gridContainer: {
    height: height * 0.3,  
    alignItems: 'center',
    marginBottom: 20,
  },
  definitionsScrollContainer: {
    height: height * 0.6,  
  },
  definitionsContainer: {
    flexDirection: 'row',
  },
  matrixContainer: {
    marginTop: 20,
  },
  matrixRow: {
    flexDirection: 'row',
  },
  matrixCell: {
    width: 15, 
    height: 15,  
    borderWidth: 1,
    borderColor: 'black',
  },
  column: {
    flex: 1,
    paddingHorizontal: 10,
  },
  definitionHeader: {
    fontWeight: 'bold',
    fontSize: 14,
    marginBottom: 10,
  },
  definitionContainer: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginTop: 5,
  },
  definitionKey: {
    fontWeight: 'bold',
    marginRight: 5,
  },
  definitionText: {
    flex: 1,
    flexWrap: 'wrap',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginVertical: 20,
    textAlign: 'center',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
    textAlign: 'center',
  },
  animal: {
    position: 'absolute',
    top: '50%',
    marginTop: -10, 
  },
});
