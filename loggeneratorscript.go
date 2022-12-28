package main

import (
	"fmt"
	"log"
	"math/rand"
	"os"
	"strconv"
	"sync"
	"time"
)

// var letters = []rune("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
var level = [5]string{"warn", "debug", "level", "trace", "info"}

/*func randSeq(n int) string {
	b := make([]rune, n)
	for i := range b {
		b[i] = letters[rand.Intn(len(letters))]
	}
	return string(b)
}
*/

func createNewLog(fileName string) *log.Logger {
	file, err := os.OpenFile(fileName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
	if err != nil {
		log.Fatal(err)
	}
	return log.New(file, "", log.Ldate|log.Ltime)
}

func produceLog(fileName string, numberofLogs int, msgLength int, rotateSize int, timeToSleep int) {
	fileCount := 0
	presentFileName := fmt.Sprintf("%s.log", fileName)
	logger := createNewLog(presentFileName)
	for count := 0; count < numberofLogs; count++ {
		fi, err := os.Stat(presentFileName)
		if err != nil {
			fmt.Println(err)
		}
		if fi.Size() > int64(rotateSize)*1000000 {
			fmt.Println("Size exceeded")
			destFile := fmt.Sprintf("%s.log.%d", fileName, fileCount)
			fileCount++
			e := os.Rename(presentFileName, destFile)
			if e != nil {
				log.Fatal(e)
			}
			logger = createNewLog(presentFileName)
		}
		// fmt.Println("in", presentFileName)
		logger.Println(level[rand.Intn(len(level))], count, "Opsramp Hyderabad")
		time.Sleep(time.Duration(timeToSleep) * time.Millisecond)
	}

}

func main() {

	numberofLogs, _ := strconv.Atoi(os.Args[1])
	numberOfFiles, _ := strconv.Atoi(os.Args[2])
	logMsgLength, _ := strconv.Atoi(os.Args[3])
	logRotateSizeInMB, _ := strconv.Atoi(os.Args[4])
	timeToSleep, _ := strconv.Atoi(os.Args[5])

	wg := new(sync.WaitGroup)

	for i := 0; i < numberOfFiles; i++ {
		wg.Add(1)
		i := i
		go func() {
			defer wg.Done()
			fileName := fmt.Sprintf("log%d", i)
			produceLog(fileName, numberofLogs, logMsgLength, logRotateSizeInMB, timeToSleep)
		}()
	}

	wg.Wait()
}
